import logging
import copy
import structlog

from tala.ddd.ddd_component_manager import DDDComponentManager
from tala.ddd.ddd_specific_components import DDDSpecificComponents
from tala.ddd.loading.component_set_loader import ComponentSetLoader
from tala.log.formats import TIS_LOGGING_COMPACT, TIS_LOGGING_NONE, TIS_LOGGING_AUTO
from tala.ddd.json_parser import JSONDDDParser
from tala.ddd.parser import Parser
from tala.ddd.services.parameters.retriever import ParameterRetriever
from tala.config import BackendConfig


class UnknownActiveDddException(Exception):
    pass


class OrchestratedDomainBundle():
    def __init__(self, args, logger=None):
        self._logger = logger or structlog.get_logger(__name__)
        self._overridden_ddd_config_paths = args.overridden_ddd_config_paths
        self._raw_config = BackendConfig(args.config).read()
        self._path = args.config or BackendConfig.default_name()
        self._repeat_questions = self._raw_config["repeat_questions"]
        self._ddd_names = self._raw_config["ddds"]
        self._rerank_amount = self._raw_config["rerank_amount"]
        self._response_timeout = self._raw_config["response_timeout"]
        self._confidence_thresholds = self._raw_config["confidence_thresholds"]
        self._confidence_prediction_thresholds = self._raw_config["confidence_prediction_thresholds"]
        self._short_timeout = self.raw_config["short_timeout"]
        self._medium_timeout = self.raw_config["medium_timeout"]
        self._long_timeout = self.raw_config["long_timeout"]
        self.ddds = self.load_ddds(self._raw_config["ddds"])
        self.active_ddd = self.get_active_ddd(self.ddds)
        self._should_greet = args.should_greet
        self._logged_tis_format = args.logged_tis_format
        self._logged_tis_update_format = args.tis_update_format
        self._log_to_stdout = args.log_to_stdout
        self._log_level = args.log_level
        if self._logged_tis_format == TIS_LOGGING_AUTO:
            log_level = logging.getLevelName(args.log_level)
            self._logged_tis_format = self._generate_tis_format_from_log_level(log_level)

    @property
    def pickle_view(self):
        copy_of_dependencies = copy.copy(self)
        copy_of_dependencies.ddds = [ddd.as_json() for ddd in self.ddds]
        return copy_of_dependencies

    def patch(self):
        self._logger.info("patching ddds")
        self._logger.info("pre patch:", self.ddds)
        ddds_as_json = self.ddds
        ddd_list = []
        for ddd_as_json in ddds_as_json:
            ddd = JSONDDDParser().parse(ddd_as_json)
            parameter_retriever = ParameterRetriever(ddd.service_interface, ddd.ontology)
            parser = Parser(ddd.name, ddd.ontology, ddd.domain.name)
            ddd_list.append(DDDSpecificComponents(ddd, parameter_retriever, parser))
        self.ddds = ddd_list
        self._logger.info("post patch:", self.ddds)

    @staticmethod
    def _generate_tis_format_from_log_level(log_level):
        if log_level == logging.DEBUG:
            return TIS_LOGGING_COMPACT
        return TIS_LOGGING_NONE

    def get_active_ddd(self, ddds):
        active_ddd_name = self._raw_config["active_ddd"]
        ddd_names = [ddd.name for ddd in ddds]
        if not active_ddd_name and len(ddd_names) == 1:
            active_ddd_name = ddd_names[0]

        if active_ddd_name is None:
            raise UnknownActiveDddException(
                "Expected active_ddd to be defined in backend config when using more than one DDD (%s), "
                "but active_ddd was undefined." % ddd_names
            )
        if active_ddd_name not in ddd_names:
            raise UnknownActiveDddException(
                "Expected active_ddd as one of %s, but got %r." % (ddd_names, active_ddd_name)
            )

        return active_ddd_name

    def load_ddds(self, ddd_names):
        ddd_component_manager = DDDComponentManager()
        component_set_loader = ComponentSetLoader(ddd_component_manager, self.overridden_ddd_config_paths)
        ddds = component_set_loader.ddds_as_list(ddd_names, rerank_amount=self.rerank_amount, logger=self._logger)
        return ddds

    @property
    def logger(self):
        return self._logger

    @property
    def active_ddd(self):
        return self._active_ddd

    @active_ddd.setter
    def active_ddd(self, active_ddd):
        self._active_ddd = active_ddd

    @property
    def should_greet(self):
        return self._should_greet

    @property
    def logged_tis_format(self):
        return self._logged_tis_format

    @property
    def logged_tis_update_format(self):
        return self._logged_tis_update_format

    @property
    def log_to_stdout(self):
        return self._log_to_stdout

    @property
    def log_level(self):
        return self._log_level

    @property
    def confidence_thresholds(self):
        return self._confidence_thresholds

    @property
    def confidence_prediction_thresholds(self):
        return self._confidence_prediction_thresholds

    @property
    def raw_config(self):
        return self._raw_config

    @property
    def overridden_ddd_config_paths(self):
        return self._overridden_ddd_config_paths

    @property
    def ddds(self):
        return self._ddds

    @ddds.setter
    def ddds(self, ddds):
        self._ddds = ddds

    @property
    def repeat_questions(self):
        return self._repeat_questions

    @property
    def ddd_names(self):
        return self._ddd_names

    @property
    def rerank_amount(self):
        return self._rerank_amount

    @property
    def response_timeout(self):
        return self._response_timeout

    @property
    def path(self):
        return self._path

    @property
    def short_timeout(self):
        return self._short_timeout

    @property
    def medium_timeout(self):
        return self._medium_timeout

    @property
    def long_timeout(self):
        return self._long_timeout
