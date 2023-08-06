import argparse
import subprocess
import sys

import boto3

from ssm_selector.instance_selector import InstanceSelector
from ssm_selector.__version__ import __version__


def print_troubleshooting_steps():
    steps = [
        "Check if the SSM agent is installed and running on the instance.",
        "Check if the instance is reachable and has an appropriate security group attached.",  # noqa
        "Verify that the IAM instance profile attached to the instance has the required permissions to use SSM.",  # noqa
        "Verify that the session manager plugin is installed on your local machine.",
    ]
    print("Troubleshooting steps:")
    for index, step in enumerate(steps, start=1):
        print(f"{index}. {step}")


def check_cli_and_plugin_installation():
    try:
        subprocess.run(
            ["aws", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print("AWS CLI is not installed. Please follow the instructions at:")
        print("https://aws.amazon.com/cli/")
        sys.exit(1)

    try:
        subprocess.run(
            ["session-manager-plugin"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        print(
            "Session Manager Plugin is not installed. Please follow the instructions at:"  # noqa
        )
        print(
            "https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html"  # noqa
        )
        sys.exit(1)


def create_session(profile):
    return boto3.Session(profile_name=profile) if profile else boto3.Session()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", "-p", help="AWS profile name", default=None)
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"ssm-selector: {__version__}",
        help="show version information",
    )

    args = parser.parse_args()

    check_cli_and_plugin_installation()

    region_name = "ap-northeast-1"
    session = create_session(args.profile)
    region_name = session.region_name

    selector = InstanceSelector(region_name=region_name)
    instance_id = selector.select_instance()

    if instance_id is None:
        print("No instance selected. Exiting.")
        sys.exit(0)

    ssm_client = session.client("ssm", region_name=region_name)

    try:
        response = ssm_client.start_session(Target=instance_id)
        session_id = response["SessionId"]
    except ssm_client.exceptions.TargetNotConnected:
        print(f"Failed to start SSM session on instance {instance_id}")
        print_troubleshooting_steps()
        sys.exit(1)

    cmd = f"aws ssm start-session --target {instance_id} --region {region_name}"
    if args.profile:
        cmd += f" --profile {args.profile}"

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"Failed to execute command on instance {instance_id}")
        print_troubleshooting_steps()
        sys.exit(1)

    ssm_client.terminate_session(SessionId=session_id)


if __name__ == "__main__":
    main()
