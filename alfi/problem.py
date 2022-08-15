from firedrake import *
from alfi.bary import BaryMeshHierarchy, bary


class NavierStokesProblem(object):

    def mesh(self, distribution_parameters):
        raise NotImplementedError

    def mesh_hierarchy(self, hierarchy, nref, callbacks, distribution_parameters):
        baseMesh = self.mesh(distribution_parameters)
        if hierarchy == "bary":
            mh = BaryMeshHierarchy(baseMesh, nref, callbacks=callbacks,
                                   reorder=True, distribution_parameters=distribution_parameters)
        elif hierarchy == "uniformbary":
            bmesh = Mesh(bary(baseMesh._topology_dm), distribution_parameters={"partition": False})
            mh = MeshHierarchy(bmesh, nref, reorder=True, callbacks=callbacks,
                               distribution_parameters=distribution_parameters)
        elif hierarchy == "uniform":
            mh = MeshHierarchy(baseMesh, nref, reorder=True, callbacks=callbacks,
                               distribution_parameters=distribution_parameters)
        else:
            raise NotImplementedError("Only know bary, uniformbary and uniform for the hierarchy.")
        return mh


    def bcs(self, Z):
        raise NotImplementedError

    def bcs_inflow(self, W):
        """Optional inflow BC used for the PCD preconditioner.
        The space `W` is the mixed Laplacian space; RT times DG is used.
        The Dirichlet value does not matter; PCD uses homogeneous BC.

        If not implemented, the `bcs()` method is used, in which case
        it assumed that the BC operates on the velocity space `W.sub(0)`
        and the Dirichlet value has inflow direction only (for validity
        of a priori estimates for preconditioner well-posedness)."""
        raise NotImplementedError

    def has_nullspace(self):
        raise NotImplementedError

    def nullspace(self, Z):
        if self.has_nullspace():
            MVSB = MixedVectorSpaceBasis
            return MVSB(Z, [Z.sub(0), VectorSpaceBasis(constant=True)])
        else:
            return None

    def char_velocity(self):
        return 1.0

    def char_length(self):
        return 1.0

    def mesh_size(self, u, domain_type):
        mesh = u.ufl_domain()
        if domain_type == "facet":
            dim = u.ufl_domain().topological_dimension()
            return FacetArea(mesh) if dim == 2 else FacetArea(mesh)**0.5
        elif domain_type == "cell":
            return CellSize(mesh)

    def rhs(self, Z):
        return None

    def relaxation_direction(self):
        return None
