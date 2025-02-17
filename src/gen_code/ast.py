import re

class Instruction:
    def __init__(self, name, *arguments):
        self.name = name
        self.arguments = arguments
        self.registers = set()
        patterns = [re.compile(r'\$(?P<register>..)'),
                    re.compile(r'[0-9]+\(\$(?P<register>..)\)'),
                    re.compile(r'\-[0-9]+\(\$(?P<register>..)\)')]
        for a in self.arguments:
            for p in patterns:
                machea = p.match(str(a))
                if machea:
                    reg = machea.group('register')
                    self.registers.add(reg)
                    break

    def __str__(self):
        if len(self.arguments) == 0:
            return f"{self.name}"
        elif len(self.arguments) == 3:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}, {self.arguments[2]}"
        elif len(self.arguments) == 2:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}, {self.arguments[1]}"
        elif len(self.arguments) == 1:
            return f"{'{:10}'.format(self.name)} {self.arguments[0]}"


class Comment(Instruction):
    def __init__(self, text):
        super().__init__('#', (text))



class MIPSDataSection:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        data_text = '\n'.join([f'\t{str(d)}' for d in self.data])
        return f'\n.data\n{data_text}\n'

class MIPSProgram:
    def __init__(self, data_section, text_section):
        self.data = data_section
        self.text = text_section

    def __str__(self):
        return f'{self.text}{self.data}'

class MIPSDataItem:
    def __init__(self, label, instruction):
        self.label = label
        self.instruction = instruction

    def __str__(self):
        return f'{self.label}:\n\t\t{str(self.instruction)}'


class MIPSFunction:
    def __init__(self, name, params, locals):
        self.name = name
        self.init_instructions = []
        self.instructions = []
        self.end_instructions = []
        self.used_regs = set(['ra', 'fp'])

        self.args_count = 0
        self.offset = {}
        self.args_code = []

        
        self.init_instructions.append(MoveInstruction('$fp', '$sp'))

        self.params_count = len(params)

        # Save args on the stack
        for i, p in enumerate(params):
            self.offset[p.id] = (len(params) - i - 1)*4

        for i, l in enumerate(locals, 1):
            self.offset[str(l)] = -i * 4

        self.init_instructions.append(
            SubuInstruction('$sp', '$sp', len(locals)*4))

        self.end_instructions.append(
            AdduInstruction('$sp', '$sp', len(locals)*4))
        if self.name == 'main':
            self.end_instructions.append(LiInstruction('$v0', 10))
            self.end_instructions.append(SyscallInstruction())
        else:
            self.end_instructions.append(JrInstruction('$ra'))

    def append_instruction(self, instruction):
        self.instructions.append(instruction)

    def update_used_reg(self, registers: set):
        self.used_regs.update(registers)

    def __str__(self):
        instructions = self.init_instructions + self.instructions
        return '\n'.join([f'{self.name}:']+[f'\t{str(i)}' for i in instructions])

class MIPSLabel:
    def __init__(self, name):
        self.name = name
        self.registers = set()

    def __str__(self):
        return f'{self.name}:\n'

class MIPSTextSection:
    def __init__(self, fucntions):
        self.fucntions = fucntions

    def __str__(self):
        functions_text = '\n'.join([str(f) for f in self.fucntions])
        return f'\n.text\n{functions_text}\n'

class SwInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sw', *arguments)

class BreakInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('break', *arguments)

class UswInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('usw', *arguments)

class MoveInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('move', *arguments)

class AsciizInst(Instruction):
    def __init__(self, *arguments):
        super().__init__(".asciiz", *arguments)


class SpaceInst(Instruction):
    def __init__(self, *arguments):
        super().__init__(".space", *arguments)

class SyscallInstruction(Instruction):
    def __init__(self):
        super().__init__('syscall')


class UlwInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('ulw', *arguments)

class LwInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('lw', *arguments)

class LaInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('la', *arguments)

class SbInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sb', *arguments)


class LbInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('lb', *arguments)

class LiInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('li', *arguments)

class SubuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('subu', *arguments)

class SubInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sub', *arguments)

class AdduInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('addu', *arguments)

class AddInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('add', *arguments)

class MultInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('mult', *arguments)

class MulInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('mul', *arguments)

class MultuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('multu', *arguments)

class DivuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('divu', *arguments)

class DivInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('div', *arguments)

class NorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('nor', *arguments)

class NotInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('not', *arguments)

class NegInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('neg', *arguments)

class NeguInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('negu', *arguments)

class OrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('or', *arguments)

class XorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('xor', *arguments)

class RemInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('rem', *arguments)

class RemuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('remu', *arguments)

class RolInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('rol', *arguments)

class RorInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('ror', *arguments)

class SrlInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('srl', *arguments)

class SllInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sll', *arguments)


class SraInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sra', *arguments)

class AbsInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('abs', *arguments)

class SltuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sltu', *arguments)

class SeqInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('seq', *arguments)

class SltInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('slt', *arguments)

class SneInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sne', *arguments)

class SleuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sleu', *arguments)

class SgeInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sge', *arguments)

class SgtInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgt', *arguments)

class SgeuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgeu', *arguments)

class SgtuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sgtu', *arguments)

class SleInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('sle', *arguments)

class JInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('j', *arguments)

class JalrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jalr', *arguments)

class JalInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jal', *arguments)

class JrInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('jr', *arguments)

class BInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('b', *arguments)

class BgeuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgeu', *arguments)

class BeqInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('beq', *arguments)

class BgtuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgtu', *arguments)

class BgtInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bgt', *arguments)

class BgeInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bge', *arguments)

class BneInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bne', *arguments)

class BleInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('ble', *arguments)


class BleuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bleu', *arguments)

class BeqzInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('beqz', *arguments)

class BltInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('blt', *arguments)

class BnezInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bnez', *arguments)

class BltuInstruction(Instruction):
    def __init__(self, *arguments):
        super().__init__('bltu', *arguments)
