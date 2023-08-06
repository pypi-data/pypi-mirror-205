from functools import reduce
from itertools import product

import numpy as np

from qibo import matrices
from qibo.backends import GlobalBackend
from qibo.config import raise_error
from qibo.quantum_info.superoperator_transformations import vectorization


def pauli_basis(
    nqubits: int,
    normalize: bool = False,
    vectorize: bool = False,
    sparse: bool = False,
    order: str = None,
    backend=None,
):
    """Creates the ``nqubits``-qubit Pauli basis.

    Args:
        nqubits (int): number of qubits.
        normalize (bool, optional): If ``True``, normalized basis is returned.
            Defaults to False.
        vectorize (bool, optional): If ``False``, returns a nested array with
            all Pauli matrices. If ``True``, retuns an array where every
            row is a vectorized Pauli matrix. Defaults to ``False``.
        sparse (bool, optional) If ``True``, retuns Pauli basis in a sparse
            representation. Default is ``False``.
        order (str, optional): If ``"row"``, vectorization of Pauli basis is
            performed row-wise. If ``"column"``, vectorization is performed
            column-wise. If ``"system"``, system-wise vectorization is
            performed. If ``vectorization=False``, then ``order=None`` is
            forced. Default is ``None``.
        backend (``qibo.backends.abstract.Backend``, optional): backend to be
            used in the execution. If ``None``, it uses ``GlobalBackend()``.
            Defaults to ``None``.

    Returns:
        ndarray or tuple: all Pauli matrices forming the basis. If ``sparse=True``
            and ``vectorize=True``, tuple is composed of an array of non-zero
            elements and an array with their row-wise indexes.
    """

    if nqubits <= 0:
        raise_error(ValueError, "nqubits must be a positive int.")

    if not isinstance(normalize, bool):
        raise_error(
            TypeError,
            f"normalize must be type bool, but it is type {type(normalize)} instead.",
        )

    if not isinstance(vectorize, bool):
        raise_error(
            TypeError,
            f"vectorize must be type bool, but it is type {type(vectorize)} instead.",
        )

    if not isinstance(sparse, bool):
        raise_error(
            TypeError,
            f"sparse must be type bool, but it is type {type(sparse)} instead.",
        )

    if vectorize and order is None:
        raise_error(ValueError, "when vectorize=True, order must be specified.")

    if sparse and not vectorize:
        raise_error(
            NotImplementedError,
            "sparse representation is not implemented for unvectorized Pauli basis.",
        )

    if backend is None:  # pragma: no cover
        backend = GlobalBackend()

    basis_single = [matrices.I, matrices.X, matrices.Y, matrices.Z]

    if nqubits > 1:
        basis_full = list(product(basis_single, repeat=nqubits))
        basis_full = [reduce(np.kron, row) for row in basis_full]
    else:
        basis_full = basis_single

    if vectorize and sparse:
        basis, indexes = [], []
        for row in basis_full:
            row = vectorization(row, order=order, backend=backend)
            row_indexes = list(np.flatnonzero(row))
            indexes.append(row_indexes)
            basis.append(row[row_indexes])
            del row
    elif vectorize and not sparse:
        basis = [
            vectorization(matrix, order=order, backend=backend) for matrix in basis_full
        ]
    else:
        basis = basis_full

    basis = backend.cast(basis)

    if normalize:
        basis /= np.sqrt(2**nqubits)

    if vectorize and sparse:
        indexes = backend.cast(indexes)

        return basis, indexes

    return basis


def comp_basis_to_pauli(
    nqubits: int,
    normalize: bool = False,
    sparse: bool = False,
    order: str = "row",
    backend=None,
):
    """Unitary matrix :math:`U` that converts operators from the Liouville
    representation in the computational basis to the Pauli-Liouville
    representation.

    The unitary :math:`U` is given by

    .. math::
        U = \\sum_{k = 0}^{d^{2} - 1} \\, \\ketbra{k}{P_{k}} \\,\\, ,

    where :math:`\\ket{P_{k}}` is the system-vectorization of the :math:`k`-th
    Pauli operator :math:`P_{k}`, and :math:`\\ket{k}` is the computational
    basis element.

    When converting a state :math:`\\ket{\\rho}` to its Pauli-Liouville
    representation :math:`\\ket{\\rho'}`, one should use ``order="system"``
    in :func:`vectorization`.

    Example:
        .. code-block:: python

            from qibo.quantum_info import random_density_matrix, vectorization, comp_basis_to_pauli
            nqubits = 2
            d = 2**nqubits
            rho = random_density_matrix(d)
            U_c2p = comp_basis_to_pauli(nqubits)
            rho_liouville = vectorization(rho, order="system")
            rho_pauli_liouville = U_c2p @ rho_liouville

    Args:
        nqubits (int): number of qubits.
        normalize (bool, optional): If ``True``, converts to the
            Pauli basis. Defaults to ``False``.
        sparse (bool, optional): If ``True``, returns unitary matrix in
            sparse representation. Default is ``False``.
        order (str, optional): If ``"row"``, vectorization of Pauli basis is
            performed row-wise. If ``"column"``, vectorization is performed
            column-wise. If ``"system"``, system-wise vectorization is
            performed. Default is ``"row"``.
        backend (``qibo.backends.abstract.Backend``, optional): backend to be
            used in the execution. If ``None``, it uses ``GlobalBackend()``.
            Defaults to ``None``.

    Returns:
        ndarray or tuple: Unitary matrix :math:`U`. If ``sparse=True``,
            tuple is composed of array of non-zero elements and an
            array with their row-wise indexes.

    """
    if backend is None:  # pragma: no cover
        backend = GlobalBackend()

    if sparse:
        elements, indexes = pauli_basis(
            nqubits,
            normalize,
            vectorize=True,
            sparse=sparse,
            order=order,
            backend=backend,
        )
        elements = np.conj(elements)

        return elements, indexes

    unitary = pauli_basis(
        nqubits, normalize, vectorize=True, sparse=sparse, order=order, backend=backend
    )

    unitary = np.conj(unitary)
    unitary = backend.cast(unitary, dtype=unitary.dtype)

    return unitary


def pauli_to_comp_basis(
    nqubits: int,
    normalize: bool = False,
    sparse: bool = False,
    order: str = "row",
    backend=None,
):
    """Unitary matrix :math:`U` that converts operators from the
    Pauli-Liouville representation to the Liouville representation
    in the computational basis.

    The unitary :math:`U` is given by

    .. math::
        U = \\sum_{k = 0}^{d^{2} - 1} \\, \\ketbra{P_{k}}{b_{k}} \\, .

    Args:
        nqubits (int): number of qubits.
        normalize (bool, optional): If ``True``, converts to the
            Pauli basis. Defaults to ``False``.
        sparse (bool, optional): If ``True``, returns unitary matrix in
            sparse representation. Default is ``False``.
        order (str, optional): If ``"row"``, vectorization of Pauli basis is
            performed row-wise. If ``"column"``, vectorization is performed
            column-wise. If ``"system"``, system-wise vectorization is
            performed. Default is ``"row"``.
        backend (``qibo.backends.abstract.Backend``, optional): backend to be
            used in the execution. If ``None``, it uses ``GlobalBackend()``.
            Defaults to ``None``.

    Returns:
        Unitary matrix :math:`U`.
    """
    if backend is None:  # pragma: no cover
        backend = GlobalBackend()

    unitary = pauli_basis(
        nqubits, normalize, vectorize=True, sparse=False, order=order, backend=backend
    )
    unitary = np.transpose(unitary)

    if sparse:
        elements, indexes = [], []
        for row in unitary:
            index_list = list(np.flatnonzero(row))
            indexes.append(index_list)
            elements.append(row[index_list])

        elements = backend.cast(elements)
        indexes = backend.cast(indexes)

        return elements, indexes

    return unitary
