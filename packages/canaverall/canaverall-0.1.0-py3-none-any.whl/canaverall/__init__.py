"""Top-level package for Canaveral"""
# canaveral/__init__.py

__app_name__ = "canaveral"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR,
    DB_READ_ERROR,
    DB_WRITE_ERROR,
    JSON_ERROR,
    ID_ERROR,
) = range(7)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
    DB_READ_ERROR: "database read error",
    DB_WRITE_ERROR: "database write error",
    ID_ERROR: "to-do id error",
}

COMPONENT_TYPES = ["webservice", "task", "cron-task", "daemon", "k8s-objects"]
TRAIT_TYPES = ["affinity", "annotations", "command", "container-image", "cpuscaler", "env", "expose", "gateway", "hostalias", "hpa", "init-container", "json-merge-patch", "json-patch",
               "k8s-update-strategy", "labels", "lifecycle", "nocalhost", "resource", "scaler", "service-account", "service-binding", "sidecar", "startup-probe", "storage", "topologyspreadconstraints"]
POLICY_TYPES = ["apply-once", "garbage-collect", "health", "override",
                "read-only", "replication", "shared-resource", "take-over", "topology"]
WORKFLOWSTEP_TYPES = ["addon-operation", "apply-app", "apply-component", "apply-deployment", "apply-object", "apply-terraform-config", "apply-terraform-provider", "build-push-image", "clean-jobs", "collect-service-endpoints", "create-config", "delete-config", "depends-on-app", "deploy",
                      "deploy-cloud-resource", "export-data", "export2config", "export2secret", "generate-jdbc-connection", "list-config", "notification", "print-message-in-status", "read-app", "read-config", "read-object", "request", "share-cloud-resource", "step-group", "suspend", "vela-cli", "webhook"]
