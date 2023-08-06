from ipykernel.kernelbase import Kernel
import subprocess, traceback, mimetypes, re

import asyncio
from asyncio.subprocess import PIPE
from asyncio import subprocess


async def _read_stream(stream, callback):
    while True:
        line = await stream.readline()
        if line: callback(line)
        else: break


async def run(command, stdoutcallback, stderrcallback):
    process = await subprocess.create_subprocess_shell(
        command, stdout=PIPE, stderr=PIPE
    )
    await asyncio.wait(
        [
            _read_stream(process.stdout, stdoutcallback),
            _read_stream(process.stderr, stderrcallback),
        ]
    )
    await process.wait()


emptymain = """
fn main() { println!(""); }
"""


def find_option(code, option_name):
  # find option in code
  option = None
  option_index = code.find(option_name)
  if option_index != -1:
    option = code[option_index + len(option_name):]
    option = option[:option.index('\n')].strip()
  return option



pattern = r'^fn\s+main\s*\('

def strip_main(code):
  # remove main method
  match = re.search(pattern, code, re.MULTILINE)
  if match:
    end = match.end()
    openedBrackets = 0
    hasFoundFirstBracket = False
    for i in range(end, len(code)):
      if code[i] == '{':
        hasFoundFirstBracket = True
        openedBrackets += 1
      elif code[i] == '}':
        openedBrackets -= 1

      if openedBrackets == 0 and hasFoundFirstBracket:
        return code[:match.start()] + code[i + 1:]
  else:
    return code



class CppKernel(Kernel):
  implementation = 'ipyrust'
  implementation_version = '1.0'
  language = 'cpp'
  language_version = '0.1'
  language_info = {
    'name': 'rust',
    'mimetype': 'text/rust',
    'file_extension': '.rs',
  }
  banner = "Custom rust kernel made by Luca Fabbian"


  known_cells = {}
  stack = []

  def send_error(self, text):
    stream_content = {'name': 'stderr', 'text': '\033[0;31m' + text + '\033[0m'}
    self.send_response(self.iopub_socket, 'stream', stream_content)

    return {'status': 'error',
      'execution_count': self.execution_count,
    }


  async def do_execute(self, code, silent, store_history=True, user_expressions=None,
    allow_stdin=False, *, cell_id=None):
    try:
      ipyrust_options = {
        "ipyrust_file": "src/main.rs",
        "ipyrust_build": None,
        "ipyrust_run": "cargo run -q",
      }

      # remove cell and following from stack
      if cell_id in self.stack:
        self.stack = self.stack[:self.stack.index(cell_id)]

      # iterate over options
      for option in ipyrust_options:
        # find option in previous stack entries
        for cell in self.stack:
          option_value = find_option(self.known_cells[cell], "$$" + option + ":")
          if option_value:
            ipyrust_options[option] = option_value

        # find option in code
        option_value = find_option(code, "$$" + option + ":")
        if option_value:
          ipyrust_options[option] = option_value

        

      # generate total code by stacking all cells
      totalcode = ""

      for cell in self.stack:
        totalcode += strip_main(self.known_cells[cell]) + "\n"
      totalcode += code + "\n"
      match = re.search(pattern, code, re.MULTILINE)
      if not match:
        totalcode += emptymain;


      # write code to file
      with open(ipyrust_options["ipyrust_file"], 'w') as f:
        f.write(totalcode)

      commands = []
      if(ipyrust_options["ipyrust_build"]):
        commands.append(ipyrust_options["ipyrust_build"])
      
      if(ipyrust_options["ipyrust_run"]):
        commands.append(ipyrust_options["ipyrust_run"])

      self.is_html_mode = False
      self.html_text = ""
      self.is_special_output_disabled = False


      def send_stdout(x):
        text = x.decode("UTF8")
        if self.is_special_output_disabled:
          self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text':  text})
          return
        
        if "$$$ipykernelr_disable_special_output$$$" in text:
          self.is_special_output_disabled = True
          return

        if self.is_html_mode:
          if "$$$ipykernelr_html_end$$$" in text:
            self.is_html_mode = False
            content = {
              'source': 'kernel',
              'data': {
                'text/html': self.html_text
              },
              'metadata' : {
                'text/html' : {
                }
              }
            }
            self.send_response(self.iopub_socket, 'display_data', content)
          else:
            self.html_text += text
          return

          

        if "$$$ipykernelr_html_start$$$" in text:

          self.is_html_mode = True
          self.html_text = ""
          return

        if "$$$ipykernelr_file$$$" in text:
          file_path = text[text.index("$$$ipykernelr_file$$$") + len("$$$ipykernelr_file$$$"):].strip()
          mimetype, encoding = mimetypes.guess_type(file_path)

          if mimetype is not None: 
            with open(file_path, mode="rb") as file_content:
              content = {
                'source': 'kernel',
                'data': {
                  mimetype: file_content.read()
                },
                'metadata' : {
                  mimetype : {
                  }
                }
              }
              self.send_response(self.iopub_socket, 'display_data', content)
          return

        self.send_response(self.iopub_socket, 'stream', {'name': 'stdout', 'text':  text})

      await run( " && ".join(commands), 
              send_stdout,
              lambda x: print(self.send_response(self.iopub_socket, 'stream', {'name': 'stderr', 'text':  '\033[0;31m' + x.decode("UTF8") + '\033[0m'})),
          )
      
      # store code
      self.known_cells[cell_id] = code
      self.stack.append(cell_id)
      
      return {'status': 'ok',
          'execution_count': self.execution_count,
      }
  
    except Exception as ex:
      return self.send_error(''.join(traceback.TracebackException.from_exception(ex).format()))



if __name__ == '__main__':
  from ipykernel.kernelapp import IPKernelApp
  IPKernelApp.launch_instance(kernel_class=CppKernel)
