from tala.ddd.domain_manager import DomainManager
from tala.model.semantic_logic import SemanticLogic


class DDDSpecificComponentsAlreadyExistsException(Exception):
    pass


class UnexpectedDeviceClassException(Exception):
    pass


class UnexpectedDomainException(Exception):
    pass


class UnexpectedOntologyException(Exception):
    pass


class UnexpectedDDDException(Exception):
    pass


class DDDComponentManager(object):
    def __init__(self):
        self.reset()

    def reset(self):
        self._components_of_ddds = {}
        self.ontologies = {}
        self.domains = {}
        self.domain_manager = DomainManager()
        self._ddds_of_domains = {}
        self._ddds_of_ontologies = {}
        self._semantic_logic = SemanticLogic(self)

    @property
    def semantic_logic(self):
        return self._semantic_logic

    def add(self, ddd_specific_components):
        if ddd_specific_components.name in self._components_of_ddds:
            raise DDDSpecificComponentsAlreadyExistsException(
                "Components for DDD '%s' already registered" % ddd_specific_components.name)
        self.add_ontology(ddd_specific_components.ontology)
        self._ddds_of_ontologies[ddd_specific_components.ontology] = ddd_specific_components
        self.add_domain(ddd_specific_components.domain)
        self._ddds_of_domains[ddd_specific_components.domain] = ddd_specific_components
        self._components_of_ddds[ddd_specific_components.name] = ddd_specific_components

    def ensure_ddd_components_added(self, ddd_components):
        if ddd_components.name not in self._components_of_ddds:
            self.add(ddd_components)

    def add_domain(self, domain):
        self.domains[domain.get_name()] = domain
        self.domain_manager.add(domain)

    def add_ontology(self, ontology):
        self.ontologies[ontology.get_name()] = ontology

    def get_components_for_all_ddds(self):
        return list(self._components_of_ddds.values())

    def get_ddd_specific_components(self, name):
        if name not in self._components_of_ddds:
            raise UnexpectedDDDException(
                "Expected one of the known DDDs {}, but got '{}'".format(list(self._components_of_ddds.keys()), name)
            )
        return self._components_of_ddds[name]

    def get_domain(self, name):
        return self.domains[name]

    def get_ontology(self, name):
        return self.ontologies[name]

    def get_device_classes(self):
        return [ddd.device_class
                for ddd in list(self._components_of_ddds.values())
                if ddd.device_class is not None]

    def get_device_handler(self, device_name):
        for ddd in list(self._components_of_ddds.values()):
            if ddd.device_class and ddd.device_class.__name__ == device_name:
                return ddd.device_handler

    def get_ddd_of_device_name(self, device_name):
        for ddd in list(self._components_of_ddds.values()):
            if ddd.device_class.__name__ == device_name:
                return ddd
        device_class_names = [ddd.device.__name__ for ddd in list(self._components_of_ddds.values())]
        raise UnexpectedDeviceClassException("Expected to find '%s' among known device classes %s but did not." %
                                             (device_name, device_class_names))

    def get_ddd_specific_components_of_ontology(self, ontology):
        if ontology not in self._ddds_of_ontologies:
            raise UnexpectedOntologyException("Expected to find '%s' among known ontologies %s but did not."
                                              % (ontology, list(self._ddds_of_ontologies.keys())))
        return self._ddds_of_ontologies[ontology]

    def get_ddd_specific_components_of_ontology_name(self, ontology_name):
        ontology = self.get_ontology(ontology_name)
        return self.get_ddd_specific_components_of_ontology(ontology)

    def reset_components_of_ddd(self, name):
        ddd_specific_components = self._components_of_ddds[name]
        ddd_specific_components.reset()
