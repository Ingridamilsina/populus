import os

from .base import (
    BaseCompilerBackend,
)
from populus.utils.filesystem import (
    is_executable_available
)


class LLLCompiler(object):
    """ TODO """
    def __init__(self):
        self.lllc_binary = os.environ.get('LLLC_BINARY', 'lllc')
        if not is_executable_available(self.lllc_binary):
            raise FileNotFoundError("lllc compiler executable not found!")

    def compile(self, bytecode_runtime=False):
        # FIXME: implement
        pass


class LLLBackend(BaseCompilerBackend):
    project_source_glob = ('*.lll')
    test_source_glob = ('test_*.lll')

    def get_compiled_contracts(self, source_file_paths, import_remappings):
        compiler  = LLLCompiler()

        self.logger.debug("Compiler Settings: %s", pprint.pformat(self.compiler_settings))

        compiled_contracts = []

        for contract_path in source_file_paths:
            code = open(contract_path).read()
            try:
                abi = open(contract_path + '.abi').read()
            except FileNotFoundError as e:
                self.logger.error(".lll files require an accompanying .lll.abi JSON ABI file!")
                raise e

            bytecode = '0x' + compiler.compile(code).hex()
            # FIXME: `lllc` currently has no option for this!
            bytecode_runtime = '0x' + compiler.compile(code, bytecode_runtime=True).hex()

            compiled_contracts.append({
                'name': os.path.basename(contract_path).split('.')[0],
                'abi': abi,
                'bytecode': bytecode,
                'bytecode_runtime': bytecode_runtime,
                'linkrefs': [],
                'linkrefs_runtime': [],
                'source_path': contract_path
            })

        return compiled_contracts
