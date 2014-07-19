#!/usr/bin/env python3

# swirlytool is the primary Swirlypy user interface tool, which is
# responsible for the running, creation, and inspection of Swirlypy
# courses.

import sys, argparse
import os
import tarfile

try:
    # XXX: We should be able to just import swirlypy here. We need to
    # set __all__ in the __init__.py of the main module.
    import swirlypy.course
except ImportError as e:
    print("Can't import a needed module.", e)
    print("Is it installed or in your PYTHONPATH?")
    sys.exit(1)

def load_course(path):
    """Helper function for subcommands which need to load courses
    predictably."""
    # Try to load the course.
    try:
        return swirlypy.course.Course.load(path)
    except FileNotFoundError as e:
        print(e)
        print("Couldn't load course; does it have course.yaml?")
        return None

def run(args):
    """Run a swirlypy course, packaged or raw."""
    course = load_course(args.course_path)
    if not course:
        return 1

    # If successful, print its description and execute it.
    course.print()
    course.execute()

def info(args):
    """Print verbose information about a course, packaged or raw."""
    course = load_course(args.course_path)
    if not course:
        return 1

    # If successful, print its description, and some other data about
    # it: including...
    course.print()

    # Whether the course is packaged in a pretty format or not.
    print("Course is", "" if course.packaged else "not", "packaged")

# XXX: This should also verify that the course can be run successfully.
def create(args):
    """Create a compressed course file."""

    # Find the base name of the course.
    basecoursename = os.path.basename(args.course_path).split(".")[0]

    # Change to the appropriate directory, so that our tar paths don't
    # get screwed up.
    os.chdir(os.path.dirname(args.course_path))
    tar = tarfile.open(basecoursename + ".tar.gz", "w|gz")
    tar.add(basecoursename)

def test(args):
    """Test a swirlypy course, packaged or raw."""
    course = load_course(args.course_path)
    if not course:
        return 1

    # If successful, print its description and run validate.
    course.print()
    course.validate()
    
def main(args):
    # If the subcommand is known and registered, pass it the arguments
    # and let it run.
    try:
        args.func(args)
    except AttributeError as e:
        print(e)
        parser.print_usage()

def parse(args):
    global parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    run_command = subparsers.add_parser("run", help="run a course from \
            a local file")
    run_command.add_argument("course_path", help="directory of or path \
        to directory containing course.yaml file")
    run_command.set_defaults(func=run)
    info_command = subparsers.add_parser("info", help=info.__doc__)
    info_command.add_argument("course_path", help="directory of or path \
        to directory containing course.yaml file")
    info_command.set_defaults(func=info)
    create_command = subparsers.add_parser("create", help=create.__doc__)
    create_command.add_argument("course_path", help="directory of or \
        path to directory containing course.yaml file")
    create_command.set_defaults(func=create)
    test_command = subparsers.add_parser("test", help=test.__doc__)
    test_command.add_argument("course_path", help="directory of or \
        path to directory containing course.yaml file")
    test_command.set_defaults(func=test)
    return parser.parse_args(args)

if __name__ == "__main__":
    sys.exit(main(parse(sys.argv[1:])))
