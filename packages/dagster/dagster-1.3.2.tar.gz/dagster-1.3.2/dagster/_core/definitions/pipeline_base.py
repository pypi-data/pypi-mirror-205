from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, AbstractSet, Optional, Sequence

from typing_extensions import Self

import dagster._check as check
from dagster._core.definitions.events import AssetKey
from dagster._core.errors import DagsterInvalidSubsetError
from dagster._core.selector import parse_solid_selection

if TYPE_CHECKING:
    from .job_definition import JobDefinition


class IPipeline(ABC):
    """IPipeline is a wrapper interface for PipelineDefinitions to be used as parameters to Dagster's
    core execution APIs.  This enables these execution APIs to operate on both in memory pipeline
    definitions to be executed in the current process (InMemoryPipeline) as well as definitions that
    can be reconstructed and executed in a different process (ReconstructablePipeline).
    """

    @abstractmethod
    def get_definition(self) -> "JobDefinition":
        pass

    @abstractmethod
    def subset_for_execution(
        self,
        solid_selection: Optional[Sequence[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ) -> "IPipeline":
        pass

    @property
    @abstractmethod
    def solids_to_execute(self) -> Optional[AbstractSet[str]]:
        pass

    @property
    @abstractmethod
    def asset_selection(self) -> Optional[AbstractSet[AssetKey]]:
        pass

    @abstractmethod
    def subset_for_execution_from_existing_pipeline(
        self,
        solids_to_execute: Optional[AbstractSet[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ) -> "IPipeline":
        pass


class InMemoryPipeline(IPipeline, object):
    def __init__(
        self,
        pipeline_def: "JobDefinition",
        solid_selection: Optional[Sequence[str]] = None,
        solids_to_execute: Optional[AbstractSet[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ):
        self._pipeline_def = pipeline_def
        self._solid_selection = solid_selection
        self._solids_to_execute = solids_to_execute
        self._asset_selection = asset_selection

    def get_definition(self) -> "JobDefinition":
        return self._pipeline_def

    def _resolve_op_selection(self, op_selection: Sequence[str]) -> AbstractSet[str]:
        # resolve a list of op selection queries to a frozenset of qualified op names
        # e.g. ['foo_op+'] to {'foo_op', 'bar_op'}
        check.list_param(op_selection, "op_selection", of_type=str)
        solids_to_execute = parse_solid_selection(self.get_definition(), op_selection)
        if len(solids_to_execute) == 0:
            raise DagsterInvalidSubsetError(
                f"No qualified ops to execute found for op_selection={op_selection}"
            )
        return solids_to_execute

    def _subset_for_execution(
        self,
        solids_to_execute: Optional[AbstractSet[str]],
        solid_selection: Optional[Sequence[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ) -> Self:
        if asset_selection:
            return InMemoryPipeline(
                self._pipeline_def.get_job_def_for_subset_selection(
                    asset_selection=asset_selection
                ),
                asset_selection=asset_selection,
            )
        if self._pipeline_def.is_subset_pipeline:
            return InMemoryPipeline(
                self._pipeline_def.parent_pipeline_def.get_pipeline_subset_def(solids_to_execute),  # type: ignore  # (possible none)
                solid_selection=solid_selection,
                solids_to_execute=solids_to_execute,
            )

        return InMemoryPipeline(
            self._pipeline_def.get_pipeline_subset_def(solids_to_execute),  # type: ignore  # (possible none)
            solid_selection=solid_selection,
            solids_to_execute=solids_to_execute,
        )

    def subset_for_execution(
        self,
        solid_selection: Optional[Sequence[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ) -> Self:
        # take a list of solid queries and resolve the queries to names of solids to execute
        solid_selection = check.opt_sequence_param(solid_selection, "solid_selection", of_type=str)
        check.opt_set_param(asset_selection, "asset_selection", of_type=AssetKey)

        check.invariant(
            not (solid_selection and asset_selection),
            "solid_selection and asset_selection cannot both be provided as arguments",
        )

        solids_to_execute = self._resolve_op_selection(solid_selection) if solid_selection else None
        return self._subset_for_execution(solids_to_execute, solid_selection, asset_selection)

    def subset_for_execution_from_existing_pipeline(
        self,
        solids_to_execute: Optional[AbstractSet[str]] = None,
        asset_selection: Optional[AbstractSet[AssetKey]] = None,
    ) -> Self:
        # take a frozenset of resolved solid names from an existing pipeline run
        # so there's no need to parse the selection
        check.opt_set_param(solids_to_execute, "solids_to_execute", of_type=str)
        check.opt_set_param(asset_selection, "asset_selection", of_type=AssetKey)

        check.invariant(
            not (solids_to_execute and asset_selection),
            "solids_to_execute and asset_selection cannot both be provided as arguments",
        )

        return self._subset_for_execution(solids_to_execute, asset_selection=asset_selection)

    @property
    def solid_selection(self) -> Sequence[str]:
        # a list of solid queries provided by the user
        return self._solid_selection  # type: ignore  # (possible none)

    @property
    def solids_to_execute(self) -> Optional[AbstractSet[str]]:
        # a frozenset which contains the names of the solids to execute
        return self._solids_to_execute

    @property
    def asset_selection(self) -> Optional[AbstractSet[AssetKey]]:
        return self._asset_selection
