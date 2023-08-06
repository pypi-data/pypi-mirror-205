import curses
import sys

import boto3


class InstanceSelector:
    def __init__(self, region_name):
        self.ec2 = boto3.resource("ec2", region_name=region_name)

    def get_instance_name(self, instance):
        for tag in instance.tags or []:
            if tag["Key"] == "Name":
                return tag["Value"]
        return instance.id

    def get_running_instances(self):
        instances = self.ec2.instances.filter(
            Filters=[{"Name": "instance-state-name", "Values": ["running"]}]
        )
        return instances

    def create_instance_list(self, instances):
        instance_list = [
            {
                "index": i,
                "instance_id": instance.id,
                "instance_name": self.get_instance_name(instance),
            }
            for i, instance in enumerate(instances)
        ]
        return instance_list

    def handle_key_press(self, key, cursor_y, instance_list):
        if key == curses.KEY_UP and cursor_y > 0:
            cursor_y -= 1
        elif key == curses.KEY_DOWN and cursor_y < len(instance_list) - 1:
            cursor_y += 1
        return cursor_y

    def select_instance(self):
        instances = self.get_running_instances()
        instance_list = self.create_instance_list(instances)

        if not instance_list:
            print("No running instances found.")
            sys.exit(1)

        instance_list.append(
            {"index": len(instance_list), "instance_name": "Cancel instance selection"}
        )

        selected_instance = self.select_instance_with_curses(instance_list)

        return selected_instance

    def select_instance_with_curses(self, instance_list):
        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        screen.keypad(True)

        cursor_y = 0

        while True:
            screen.clear()
            screen.addstr(
                0, 0, "Select an instance (line number to move, enter to select):"
            )
            for i, instance in enumerate(instance_list):
                screen.addstr(
                    i + 1, 0, "{:>3}: {}".format(i + 1, instance["instance_name"])
                )
                if i == cursor_y:
                    screen.chgat(i + 1, 0, -1, curses.A_REVERSE)

            screen.refresh()

            key = screen.getch()

            cursor_y = self.handle_key_press(key, cursor_y, instance_list)

            if key == curses.KEY_ENTER or key == 10:
                if cursor_y == len(instance_list) - 1:
                    selected_instance = None
                    break
                else:
                    selected_instance = instance_list[cursor_y]["instance_id"]
                    break

        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

        return selected_instance
