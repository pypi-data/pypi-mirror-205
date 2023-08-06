from itertools import product
from math import ceil
from ase import neighborlist, Atoms
from ase.io import read
from ase.visualize import view
from phonopy.interface.vasp import read_vasp
from phonopy.structure.atoms import PhonopyAtoms
import numpy as np
import numpy.linalg as la
import xyz_py as xyzp
import spglib
import warnings
import itertools
import copy
import molvis.core as mvis
import matplotlib.cm as cm

def flatten(_list):
    """
    Flattens a list of lists by one subdimension

    e.g. [[1,2,3],[[2,3,4]]] ---> [1,2,3, [2,3,4]]

    Parameters
    ----------
    _list : list
        List of lists to be flattened

    Returns
    -------
    list
        Input list of lists flattened by one subdimension
    """

    _flist = list(itertools.chain(*_list))

    return _flist


class Molecule():

    """
    Contains structural information for a single molecule

    Attributes
    ----------

    formula : str
        Chemical formula as string
    indices : list
        Indices of each atom relative to supercell
    fragment_ind : list of lists
        List of lists, each containg a fragment of the molecule which is
        obtained when periodic boundary conditions are not considered
    dis_bonds : list of lists
        List of 2 element lists containing atomic indices specifying which
        bonds disappear when periodic boundary conditions are not considered

    """

    __slots__ = 'formula', 'indices', 'fragment_indices', 'dis_bonds'

    def __init__(self, formula, indices):

        self.formula = formula
        self.indices = indices
        self.fragment_indices = [[], [], []]
        self.dis_bonds = [[], [], []]

        return

    def add_fragments(self, axis, fragment_indices, dis_bonds):

        self.fragment_indices[axis] = fragment_indices
        self.dis_bonds[axis] = dis_bonds

        return


def calculate_molecule_shifts(molecule: Molecule, coords: list[list[float]],
                              lat_vecs: list[float]) -> list[float]:
    """
    Calculates translation operations required to reassemble
    current molecule from its constituent fragments

    Parameters
    ----------
    molecule : Molecule
        Molecule object for current molecule
    coords : list[list[float]]
        coordinates of full supercell
    lat_vecs : list[list[float]]
        lattice vectors of full supercell

    Returns
    -------
    list[float]
        Shift for each atom of cell in cartesian coordinates
    """

    shifts = np.zeros(np.shape(coords))

    n_atoms = len(molecule.indices)

    _atoms = Atoms(
        numbers=np.ones(n_atoms),
        positions=coords[molecule.indices],
        cell=lat_vecs,
        pbc=[True, True, True]
    )

    inds_to_order = {
        ind: it for it, ind in enumerate(molecule.indices)
    }

    pbc_distances = _atoms.get_all_distances(mic=True)

    for ax_it in range(3):
        for atom_a, atom_b in molecule.dis_bonds[ax_it]:

            pos_ps = np.where(shifts[atom_a] >= 1., 1., 0.)
            neg_ps = np.where(shifts[atom_a] <= -1., -1., 0.)

            pre_shift = (pos_ps + neg_ps) @ lat_vecs

            # Calculate distance between two atoms, accounting
            # for any shifts that are to be applied
            # This avoids double shifting back and forth
            dist = (coords + pre_shift)[atom_a, ax_it] - coords[atom_b, ax_it]

            # If distance is small now shifts have been applied then skip
            if np.abs(dist) < 1.05*pbc_distances[inds_to_order[atom_a], inds_to_order[atom_b]]: # noqa
                continue
            # Else, find other fragment indices and shift
            for fragi in molecule.fragment_indices[ax_it]:
                if atom_b in fragi:
                    fragi_b = fragi
            # Add 1 count of lattice vector to atom
            shifts[fragi_b, ax_it] += int(dist/np.abs(dist))

    # Avoid double shifting by the same lattice vector
    pos = np.where(shifts >= 1., 1., 0.)
    neg = np.where(shifts <= -1., -1., 0.)
    shifts = pos + neg

    cart_shifts = shifts @ lat_vecs

    return cart_shifts


class Cell():
    """
    Contains information on a given cell, unit or otherwise.

    Parameters
    ----------
    lat_vecs : np.array
        Lattice vectors as rows
    frac_coords : np.array
        Fractional coordinates of each atom in cell [a, b, c]
    atom_numbers : list[int]
        Atomic number of each atom in cell
    adjust_cutoff : dict
        Keys are element symbols values the new cut-offs

    Attributes
    ----------
    lat_vecs : np.array
        Lattice vectors as rows
    cell_params : list
        Cell parameters (norm of lattice vectors) [a, b, c]
    frac_coords : np.array
        Fractional coordinates of each atom in cell [a, b, c]
    cart_coords : np.array
        Cartesian coordinates of each atom
    atom_numbers : list[int]
        Atomic number of each atom in cell
    atom_labels : list[str]
        Atomic label of each atom in cell
    molecules : list[Molecules]
        cells.Molecule objects, one per complete entity in the unit cell
    symmetry : dict
        spglib.get_symmetry_dataset output
    repair_shifts : np.array
        Cartesian shifts which, when applied to the cartesian coordinates of
        the cell, repair the cell edges such that complete entities are present
        rather than fragments connected by periodic boundary conditions

    Returns
    -------
        None
    """

    __slots__ = [
        'lat_vecs', 'frac_coords', 'atom_numbers', 'cart_coords',
        'cell_params', 'atom_labels', 'atom_labels_nn', 'molecules',
        'symmetry', 'repair_shifts', 'asu_entities'
    ]

    def __init__(self, lat_vecs, frac_coords, atom_numbers,
                 adjust_cutoff=None):

        self.lat_vecs = lat_vecs
        self.frac_coords = frac_coords
        self.atom_numbers = atom_numbers

        self.cell_params = la.norm(self.lat_vecs, axis=1)

        # Convert atomic numbers to labels
        self.atom_labels = np.array(
            xyzp.num_to_lab(self.atom_numbers, numbered=False)
        )

        self.atom_labels_nn = np.array(
            xyzp.remove_label_indices(
                self.atom_labels
            )
        )

        # Convert fractional to cartesian coordinates
        self.cart_coords = self.frac_coords @ self.lat_vecs

        # Placeholder for list of molecules
        self.molecules = []

        # Find symmetry dataset
        self.symmetry = spglib.get_symmetry_dataset(
            (
                self.lat_vecs,
                self.frac_coords,
                self.atom_numbers
            )
        )

        # Find translations that repair edges of supercell to
        # give complete molecules
        self.repair_shifts = self.find_repair_shifts()

        # Find indices of whole, unique, entities in the asymmetric unit (ASU)
        # Entities are molecules, anions, cations
        # Keys of dictionary are formulae
        # e.g. H20_1, H20_2, ....
        # and values are list of indices of that entity relative to
        # supercell coordinates
        self.asu_entities = self.find_asu_entities(adjust_cutoff=adjust_cutoff)
        return

    @classmethod
    def from_phonopyatoms(cls, phonopy_atoms: PhonopyAtoms):
        """
        Creates cell object from PhonopyAtoms object
        """
        return cls(*phonopy_atoms.totuple())

    @classmethod
    def from_cif(cls, cif_file):
        """
        Creates cell object from cif file
        """

        # Ignore incorrect ase warning about space group
        warnings.filterwarnings("ignore", category=UserWarning)
        atoms = read(cif_file)

        return cls(
            atoms.cell,
            atoms.get_scaled_positions(),
            atoms.get_atomic_numbers()
        )

    def shift_centre_to(self,
                        new_frac_centre: list[float, float, float]) -> None:
        """
        Periodically shifts centre of cell to new point in fractional
        coordinates, and  recalculates cartesian coordinates to match

        Parameters
        ----------
        new_frac_centre : list[float, float, float]
            Fractional coordinates of new cell centre [a, b, c]

        Returns
        -------
            None
        """

        self.frac_coords += ([0.5, 0.5, 0.5] - new_frac_centre)
        self.frac_coords %= 1.
        self.cart_coords = self.frac_coords @ self.lat_vecs

        return

    @staticmethod
    def _get_adjacency(labels: list[str], coords: list, vecs: list,
                       pbc: list[bool, bool, bool] = [True, True, True],
                       visualise: bool = False) -> list:
        """
        Calculate adjacency matrix using ASE with or without periodic boundary
        conditions

        Parameters
        ----------
        labels : list
            Atomic labels
        coords : np.ndarray
            xyz coordinates as (n_atoms, 3) array
        vecs : np.ndarray
            Lattice vectors as (3,3) array
        pbc : list[bool], default [True, True, True]
            If true, apply periodic boundary conditions along specified cell
            axis [a, b, c]
        visualise : bool, default False
            If true, show cell in interactive 3d display

        Returns
        -------
        np.array
            Adjacency matrix with same order as labels/coords
        """

        # Make box
        box = Atoms(
            symbols=labels,
            positions=coords,
            cell=vecs,
            pbc=pbc
        )

        if visualise:
            view(box)

        # Define cutoffs for each atom using atomic radii
        cutoffs = neighborlist.natural_cutoffs(box)

        # Create neighbourlist using cutoffs
        neigh_list = neighborlist.NeighborList(
            cutoffs=cutoffs,
            self_interaction=False,
            bothways=True
        )

        # Update this list by specifying the atomic positions
        neigh_list.update(box)

        # Create adjacency matrix
        adjacency = neigh_list.get_connectivity_matrix(sparse=False)

        return adjacency

    def get_adjacency(self,
                      pbc: list[bool, bool, bool]
                      = [True, True, True]) -> list:
        """
        Calculate adjacency matrix using ASE with or without periodic boundary
        conditions

        Parameters
        ----------
        pbc : list[bool], default [True, True, True]
            If true, apply periodic boundary conditions along specified cell
            axis [a, b, c]
        Returns
        -------
        np.array
            Adjacency matrix with same order as labels/coords
        """

        adjacency = Cell._get_adjacency(
            self.atom_labels_nn,
            self.cart_coords,
            self.lat_vecs,
            pbc,
            visualise=False
        )

        return adjacency

    def get_entities(self,
                     pbc: list[bool, bool, bool] = [True, True, True]) -> dict:
        """
        Find entities in cell using ASE with or without periodic boundary
        conditions

        Parameters
        ----------
        pbc : list[bool], default [True, True, True]
            If true, apply periodic boundary conditions along specified cell
            axis [a, b, c]

        Returns
        -------
        dict
            keys = molecular formula,
            vals = list of lists, where each list contains the indices of a
                   single occurrence of the `key`, and the indices match the
                   order given in `labels` and `coords`

        """

        adjacency = self.get_adjacency(pbc)

        entities = xyzp.find_entities_from_adjacency(
            self.atom_labels_nn,
            adjacency
        )

        return entities

    def print_space_group(self):

        print("Structure is {}".format(self.symmetry["international"]))

        return

    def find_centre_indices(self, central_formula: str) -> tuple[list, list]:
        """
        Finds indices of entity with formula `central_formula`
        closest to centre of cell.

        Indices are given relative to full list of cell coordinates
        and atom labels

        Parameters
        ----------
        central_formula : str
            Formula string of central molecule

        Returns
        -------
        list
            Indices of central entity with `central_formula` in cell
        list
            Indices of environment (everything other than central entity)
            in cell
        """

        # Create adjacency matrix with periodic boundary conditions in all
        # directions
        entities_pbc = self.get_entities()

        # Indices of every instance of the central molecule
        all_cent_ent_indices = flatten(entities_pbc[central_formula])

        # Of the choices of central molecule, find the indices of the one
        # closest to the middle of the cell
        centre = np.sum(self.lat_vecs / 2., axis=1)
        closest_index = np.argmin(
            la.norm(
                self.cart_coords[all_cent_ent_indices] - centre,
                axis=1
            )
        )
        closest_index = all_cent_ent_indices[closest_index]

        environment_entities = copy.deepcopy(entities_pbc)

        for it, indices in enumerate(entities_pbc[central_formula]):
            if closest_index in indices:
                central_indices = indices
                environment_entities[central_formula].pop(it)

        environment_indices = flatten(
            flatten(
                environment_entities.values()
            )
        )

        return central_indices, environment_indices

    def find_repair_shifts(self):
        """
        Calculates translation operations required to "repair" molecules at
        the boundary of the supercell such that they are whole again
        """

        # Create adjacency matrix with periodic boundary conditions in all
        # directions
        adjacency_pbc = self.get_adjacency(
            pbc=[True, True, True]
        )

        # Find entities (molecules or otherwise) using adjacency matrix
        entities_pbc = xyzp.find_entities_from_adjacency(
            self.atom_labels_nn, adjacency_pbc
        )

        # Make list of molecules, which will tie fragments to full sets of
        # indices
        molecules = [
            Molecule(formula, full_mol)
            for formula, entities in entities_pbc.items()
            for full_mol in entities
        ]

        # Periodic boundary conditions deactivated for one of eac
        # direction
        pbc_choices = [
            [False, True, True],
            [True, False, True],
            [True, True, False],
        ]

        # Disable PBC in one cell direction, calculate adjacency, entities, and
        # find which bonds are cut
        for ax_it in range(3):
            adjacency_no_pbc = Cell._get_adjacency(
                self.atom_labels_nn, self.cart_coords, self.lat_vecs,
                pbc=pbc_choices[ax_it], visualise=False
            )

            entities_no_pbc = xyzp.find_entities_from_adjacency(
                self.atom_labels_nn, adjacency_no_pbc
            )

            # Find bonds which disappear when PBC disabled along current axis
            missing_bonds = np.array(
                np.nonzero(adjacency_pbc - adjacency_no_pbc)
            ).T

            entities_no_pbc_ind = flatten(entities_no_pbc.values())

            for molecule in molecules:

                # Collect fragments which make up current molecules
                fragments = [
                    [fra for fra in frag if fra in molecule.indices]
                    for frag in entities_no_pbc_ind
                ]
                # Remove None elements
                fragments = list(filter(None, fragments))
                # Find bonds which disappear when PBC deactivated
                dis_bonds = [
                    [atom_1, atom_2]
                    for atom_1, atom_2 in missing_bonds
                    if atom_1 in molecule.indices
                    and atom_2 in molecule.indices
                ]
                # Reorder fragment indices to have largest fragment first and
                # smallest last
                fragments = sorted(fragments, key=len, reverse=True)

                # Reorder disappearing bonds to be [large frag, small frag]
                tmp = []
                for atom_1, atom_2 in dis_bonds:
                    for frag in fragments:
                        if atom_1 in frag:
                            la1 = len(frag)
                        elif atom_2 in frag:
                            la2 = len(frag)
                    if la2 > la1:
                        tmp.append([atom_2, atom_1])
                    else:
                        tmp.append([atom_1, atom_2])
                dis_bonds = tmp

                molecule.add_fragments(ax_it, fragments, dis_bonds)

        self.molecules = molecules

        # For each molecule, check disconnected bonds and record shift
        # required to mend them. Shift is a lattice parameter
        repair_shift = np.zeros([self.atom_labels.size, 3])
        for molecule in molecules:
            if not len(molecule.dis_bonds):
                continue
            repair_shift += calculate_molecule_shifts(
                molecule, self.cart_coords, self.lat_vecs
            )

        return repair_shift

    def find_asu_entities(self, adjust_cutoff=None) -> dict:
        """
        Finds unique molecules of supercell by permuting unique atoms
        to give minimum number of molecules required to rebuild unit cell

        Returns
        -------
        dict
            keys are formula string of entity
            values are list of lists, each sublist containing indices of
            entity
        """

        asu_indices = np.unique(self.symmetry['equivalent_atoms'])

        n_unique = len(asu_indices)

        # Enforce that asymmetric unit atoms are of same molecules
        # since complete bonding has been traced, can just start with first
        # atom and go from there
        assignments = [False] * n_unique
        new_asu_indices = []

        asu_indices_to_assignment = {
            asu_index: it for it, asu_index in enumerate(asu_indices)
        }

        for it, asu_index in enumerate(asu_indices):
            # If this atom or one of its symmetrical equivalents
            # has already been included then skip
            if assignments[it]:
                continue

            # Else, find the molecule to which this unique atom belongs
            for molecule in self.molecules:
                if asu_index in molecule.indices:
                    # and add it to the new list of unique atoms
                    new_indices = copy.deepcopy(molecule.indices)

            # Update the assignment list to include new unique atoms
            for index in new_indices:
                new_asu_indices.append(index)
                assignments[
                    asu_indices_to_assignment[
                        self.symmetry["equivalent_atoms"][index]
                    ]
                ] = True

        asu_indices = new_asu_indices

        # Find entities in asymmetric unit
        # N.B. Indexing here is according to ASU subset, not full unit cell
        asu_ents = xyzp.find_entities(
            self.atom_labels_nn[asu_indices],
            (self.cart_coords + self.repair_shifts)[asu_indices],
            adjust_cutoff=adjust_cutoff
        )

        # Switch entity indexing to full unit cell
        new_asu_ents = {
            entity: [
                [asu_indices[ind] for ind in indices]
                for indices in full_indices
            ] for entity, full_indices in asu_ents.items()
        }

        # Create new list of equivalent atoms
        # using whole entities as unique atoms to which
        # all others are equivalent
        new_equiv = self.symmetry['equivalent_atoms']

        for new in asu_indices:
            old = self.symmetry['equivalent_atoms'][new]
            new_equiv[np.where(new_equiv == old)] = new

        self.symmetry['equivalent_atoms'] = new_equiv

        new_asu_ents = {
            "{}_{:d}".format(formula, it+1): indices
            for formula, all_indices in new_asu_ents.items()
            for it, indices in enumerate(all_indices)
        }

        return new_asu_ents

    def reconstruct_from_asu_unit(self):

        # Rotate lattice vectors into standard basis
        _standard_lat_vecs = (
            self.lat_vecs.T @ self.symmetry["transformation_matrix"]
        ).T

        # Shift origin of coordinate system
        _standard_frac_coords = np.array([
            coord + self.symmetry["origin_shift"]
            for coord in self.frac_coords
        ])

        # Rotate standard lattice vectors into idealised basis
        _ideal_lat_vecs = (
            self.symmetry["std_rotation_matrix"] @ _standard_lat_vecs.T
        ).T

        rotations = self.symmetry['rotations']
        translations = self.symmetry['translations']

        # Some sort of origin shift is required here but is not
        # performed by spglib
        # for it in range(306):
        #     self.frac_coords[it] += np.diag(
        # np.array([[-0.5, 0., 0.],[0, -0.5, 0.],[0., 0., -0.5]])
        # )

        asu_indices = np.unique(self.symmetry['equivalent_atoms'])

        recon_f_coords = np.vstack([
            (rot @ _standard_frac_coords[asu_indices].T).T + trans
            for rot, trans in zip(rotations, translations)
        ])

        recon_c_coords = recon_f_coords @ _ideal_lat_vecs

        recon_labels = [self.atom_labels_nn[asu_indices]]
        recon_labels *= rotations.shape[0]
        recon_labels = np.concatenate(recon_labels)

        return recon_c_coords, recon_labels


class DistortionExpansion:
    """
    Contains information on supercell created from a given cell with
    specified expansion

    Parameters
    ----------
    lat_vecs : list
        Lattice vectors of unit cell as rows
    frac_coords : list
        Coordinates of each atom in cell as fraction of cell parameters
    atom_numbers : list
        Atomic number of each atom in cell
    expansion : list[int]
        Requested (integer) supercell expansion e.g. [3, 3, 3]

    Attributes
    ----------
    expansion : list[int]
        Expansion used to generate supercell from cell e.g. [3, 3, 3]
    uc_sc_map : list
        Mapping of supercell atoms onto unit cell atoms
    """
    def __init__(self, lat_vecs, coords, atom_numbers, *args, **kwargs) -> None:

        self.lat_vecs = lat_vecs
        self.coords = self.recenter_unitcell(coords, *args)
        self.atom_numbers = atom_numbers

        self.cart_coords = self.generate_cluster(*args)
        self.frac_coords = self.cart_coords @ la.inv(self.lat_vecs)
        self.n_atoms = len(atom_numbers)
        self.n_cell = self.frac_coords.shape[0] // self.coords.shape[0]

    @classmethod
    def from_poscar(cls, poscar_name, *args):
        atoms = read_vasp(poscar_name)
        return cls(atoms.cell, atoms.scaled_positions, atoms.numbers, *args)

    def generate_cluster(self, *args):
        
        def shift_coords(idc):
            return (self.coords + np.array(idc)) @ self.lat_vecs

        coords = np.array([coord for idc in self.generate_cell_idc(*args)
                           for coord in shift_coords(idc)])

        return self.recenter_cluster(coords, *args)


class DistortionSupercell(DistortionExpansion):

    def generate_cell_idc(self, expansion):

        def expansion_range(num):

            start = stop = num // 2

            if num % 2 == 0:  # even
                return range(-start, stop)
            elif num % 2 == 1:  # odd
                return range(-start, stop + 1)

        for nvec in product(*map(expansion_range, expansion)):
            yield nvec

    def recenter_cluster(self, cart, expansion):

        def shift(num, vec):
            if num % 2 == 0:  # even
                return 0.0
            elif num % 2 == 1:  # odd
                return vec / 2
            
        return cart - np.sum(list(map(shift, expansion, self.lat_vecs)), axis=0)

    def recenter_unitcell(self, frac, expansion):

        def shift(num):
            if num % 2 == 0:  # even
                return 0.0
            elif num % 2 == 1:  # odd
                return 1 / 2
            
        return frac + np.array(list(map(shift, expansion)))


class DistortionCluster(DistortionExpansion):

    def generate_cell_idc(self, cutoff):

        def expansion_range(vec):
            num = ceil(cutoff / np.linalg.norm(vec))
            return range(-num, num + 1)

        for nvec in product(*map(expansion_range, self.lat_vecs)):

            r = np.sum([ni * ci for ni, ci in zip(nvec, self.lat_vecs)], axis=0)

            if np.linalg.norm(r) <= cutoff:
                yield nvec

    def recenter_cluster(self, cart, *args):
        return cart - np.sum(self.lat_vecs, axis=0) / 2

    def recenter_unitcell(self, frac, *args):
        return (frac + 1 / 2) % 1.0


def write_molcas_basis(labels, charge_dict, name):
    """
    Writes dummy molcas basis file for environment charges to a textfile named
    according to the basis name.

    Parameters
    ----------
    labels : list[str]
        Atomic labels of environment with no indexing
    charge_dict : dict
        CHELPG charge of each environment atom
    name : str
        Root name of basis
    """

    labels = xyzp.remove_label_indices(labels)

    with open(name, 'w') as f:

        f.write("* This file was generated by spin_phonon_suite\n")
        for elem, (lab, chrg) in zip(labels, charge_dict.items()):
            f.write(f"/{elem}.{name}.{lab}.0s.0s.\n")
            f.write("Dummy basis set for atomic charges of environment\n")
            f.write("no ref\n")
            f.write(f"{chrg:.9f} 0\n")
            f.write("0 0\n")

    return


def vis_charges_viewer(coords, labels, norm_charges, extra_coords=[],
                       extra_labels=[], extra_color='', viewer_style_args={},
                       viewer_div_args={}, main_kwargs={}, extra_kwargs={}):

    ms1 = mvis.Model(labels, coords, **main_kwargs)

    colours = cm.get_cmap('coolwarm', 250)

    ms1.atom_colours = [
        '#{0:02x}{1:02x}{2:02x}'.format(*col[:-1])
        for col in colours(norm_charges, bytes=True)
    ]

    ms2 = mvis.Model(extra_labels, extra_coords, **extra_kwargs)

    if extra_color:
        ms2.atom_colours = extra_color

    viewer = mvis.Viewer(
        objects=[ms1, ms2],
        extra_div_args=viewer_div_args,
        extra_style_args=viewer_style_args
    )

    return viewer
