from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.validator import EmptyInputValidator, NumberValidator

from canaverall import COMPONENT_TYPES, POLICY_TYPES, TRAIT_TYPES, WORKFLOWSTEP_TYPES

used_component_names = []
used_workflowstep_names = []

def create_choice_list_component(components: list[dict]):
    choice_list = []
    for idx, component in enumerate(components):
        choice_list.append(Choice(name=component["name"], value=idx))
    return choice_list


def validator_name(name: str) -> bool:
    return True if len(name) <= 63 and name[0].isalnum() and name[-1].isalnum() and all(
        [char.isalnum() or char in ["-", "_", "."] for char in name]) else False


def validator_component_name(name: str) -> bool:
    # The name segment is required and must be 63 characters or less,
    # beginning and ending with an alphanumeric character ([a-z0-9A-Z])
    # with dashes (-), underscores (_), dots (.), and alphanumerics between.
    # It cannot be empty or contain spaces.
    # It cannot be repeated between component names
    return True if len(name) <= 63 and name[0].isalnum() and name[-1].isalnum() and all(
        [char.isalnum() or char in ["-", "_", "."] for char in name]) and name not in used_component_names else False

def validator_workflowstep_name(name: str) -> bool:
    # The name segment is required and must be 63 characters or less,
    # beginning and ending with an alphanumeric character ([a-z0-9A-Z])
    # with dashes (-), underscores (_), dots (.), and alphanumerics between.
    # It cannot be empty or contain spaces.
    # It cannot be repeated between workflowstep names
    return True if len(name) <= 63 and name[0].isalnum() and name[-1].isalnum() and all(
        [char.isalnum() or char in ["-", "_", "."] for char in name]) and name not in used_workflowstep_names else False


def oam_form():
    oam_file_data = {}
    used_component_names.clear()

    oam_file_data["app_name"] = inquirer.text(
        message="What is the name of the application?",
        validate=validator_name,
    ).execute()

    # COMPONENTS
    oam_file_data["components"] = []
    components_number = 1

    print('Provide details for the first component:')
    component_name = inquirer.text(
        message="What is the name of the component?",
        validate=validator_component_name,
    ).execute()
    component_type = inquirer.fuzzy(
        message=f'What is the type of component "{component_name}"?',
        choices=COMPONENT_TYPES,
    ).execute()
    component_image = inquirer.text(
        message=f'What is the Docker image of component "{component_name}"?',
        validate=EmptyInputValidator(),
    ).execute()
    component = {"name": component_name,
                 "type": component_type,
                 "image": component_image,
                 }
    oam_file_data["components"].append(component)
    used_component_names.append(component_name)

    another_component = inquirer.confirm(
        message="Do you want to add another component?",
    ).execute()
    while another_component:
        components_number += 1
        component_name = inquirer.text(
            message="What is the name of the component?",
            validate=validator_component_name,
        ).execute()
        component_type = inquirer.fuzzy(
            message=f'What is the type of component "{component_name}"?',
            choices=COMPONENT_TYPES,
        ).execute()
        component_image = inquirer.text(
            message=f'What is the Docker image of component "{component_name}"?',
            validate=EmptyInputValidator(),
        ).execute()
        component = {"name": component_name,
                     "type": component_type,
                     "image": component_image,
                     }
        oam_file_data["components"].append(component)
        used_component_names.append(component_name)
        another_component = inquirer.confirm(
            message="Do you want to add another component?",
        ).execute()

    # TRAITS
    mess = "Do you want to add traits to any of the components?" if components_number > 1 else (
          f"Do you want to add traits to the component {component_name}?")
    traits = inquirer.confirm(
        message=mess,
    ).execute()

    while traits:
        if components_number == 1:
            current_comp_idx: int = 0
        else:
            print(f'There are {components_number} components')
            current_comp_idx: int = int(inquirer.rawlist(
                message="Which component do you want to add traits to?",
                choices=create_choice_list_component(
                    oam_file_data["components"]),
                default=None,
            ).execute())

        print(f"current_comp_idx -> {current_comp_idx}")
        oam_file_data["components"][current_comp_idx]["traits"] = [] if "traits" not in oam_file_data["components"][
            current_comp_idx] else oam_file_data["components"][current_comp_idx]["traits"]

        trait_type = inquirer.fuzzy(
            message="What is the type of the trait?",
            choices=TRAIT_TYPES,
        ).execute()
        trait = {"type": trait_type}
        oam_file_data["components"][current_comp_idx]["traits"].append(trait)

        another_trait = inquirer.confirm(
            message=f"Do you want to add another trait to component {oam_file_data['components'][current_comp_idx]['name']}?",
        ).execute()
        while another_trait:
            trait_type = inquirer.fuzzy(
                message="What is the type of the trait?",
                choices=TRAIT_TYPES,
            ).execute()
            trait = {"type": trait_type}
            oam_file_data["components"][current_comp_idx]["traits"].append(trait)
            another_trait = inquirer.confirm(
                message="Do you want to add another trait to the component?",
            ).execute()

        if components_number > 1:
            traits = inquirer.confirm(
                message="Do you want to add more traits to any of the components?",
            ).execute()
        else:
            traits = False

    # POLICIES

    policies = inquirer.confirm(
        message="Do you want to add policies to the application?",
    ).execute()

    if policies:
        oam_file_data["policies"] = []

        policy_type = inquirer.fuzzy(
            message="What is the type of the policy?",
            choices=POLICY_TYPES,
        ).execute()
        policy_name = inquirer.text(
            message="What is the name of the policy?",
            validate=validator_name,
        ).execute()
        policy = {"name": policy_name,
                    "type": policy_type,
                    }
        oam_file_data["policies"].append(policy)

        another_policy = inquirer.confirm(
            message="Do you want to add another policy?",
        ).execute()
        while another_policy:
            policy_type = inquirer.fuzzy(
                message="What is the type of the policy?",
                choices=POLICY_TYPES,
            ).execute()
            policy_name = inquirer.text(
                message="What is the name of the policy?",
                validate=validator_name,
            ).execute()
            policy = {"name": policy_name,
                        "type": policy_type,
                        }
            oam_file_data["policies"].append(policy)
            another_policy = inquirer.confirm(
                message="Do you want to add another policy?",
            ).execute()

    # WORKFLOW

    workflow = inquirer.confirm(
        message="Do you want to add a workflow to the application?",
    ).execute()

    if workflow:
        used_workflowstep_names.clear()
        print("The workflow is composed of a list of steps")
        workflow_step_type = inquirer.fuzzy(
            message="What is the first step?",
            choices=WORKFLOWSTEP_TYPES,
        ).execute()
        workflow_step_name = inquirer.text(
            message="What is the name of the first step?",
            validate=validator_workflowstep_name,
        ).execute()
        workflow_step = {"name": workflow_step_name,
                            "type": workflow_step_type,
                            }
        oam_file_data["workflow"].append(workflow_step)

        another_step = inquirer.confirm(
            message="Do you want to add another step?",
        ).execute()
        while another_step:
            workflow_step_type = inquirer.fuzzy(
                message="What is the next step?",
                choices=WORKFLOWSTEP_TYPES,
            ).execute()
            workflow_step_name = inquirer.text(
                message="What is the name of the next step?",
                validate=validator_workflowstep_name,
            ).execute()
            workflow_step = {"name": workflow_step_name,
                                "type": workflow_step_type,
                                }
            oam_file_data["workflow"].append(workflow_step)
            another_step = inquirer.confirm(
                message="Do you want to add another step?",
            ).execute()

    return oam_file_data
