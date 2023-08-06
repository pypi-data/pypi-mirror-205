#!/usr/bin/env cwl-runner
# Example command line program wrapper for the Unix tool "sort"
# demonstrating command line flags.
class: CommandLineTool
doc: "Sort lines using the `sort` command"
cwlVersion: v1.0

# This example is similar to the previous one, with an additional input
# parameter called "reverse".  It is a boolean parameter, which is
# interpreted as a command line flag.  The value of "prefix" is used for
# flag to put on the command line if "reverse" is true, if "reverse" is
# false, no flag is added.
#
# This example also introduced the "position" field.  This indicates the
# sorting order of items on the command line.  Lower numbers are placed
# before higher numbers.  Here, the "--reverse" flag (if present) will be
# added to the command line before the input file path.
inputs:
  - id: reverse
    type: boolean
    inputBinding:
      position: 1
      prefix: "--reverse"
  - id: sorted_input
    type: File
    inputBinding:
      position: 2

outputs:
  - id: sorted_output
    type: File
    outputBinding:
      glob: output.txt

baseCommand: sort
stdout: output.txt
