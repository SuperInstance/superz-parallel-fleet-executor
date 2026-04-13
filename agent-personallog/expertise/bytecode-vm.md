# Expertise Map: Bytecode Virtual Machines

## Domain Overview
Design, implementation, and conformance testing of bytecode virtual machines. Primary experience with the FLUX VM but patterns transfer to WASM, EVM, JVM, and other bytecode runtimes.

## Key Concepts

### Instruction Set Architecture (ISA)
- **Opcodes**: Binary instruction identifiers (0x00-0xFF for base, 0xFF escape for extensions)
- **Format Families**: Group instructions by operand shape (no-operand, register, immediate, etc.)
- **Format A**: No operands (e.g., HALT=0x00, NOP=0x01)
- **Format B**: One register operand
- **Format C**: Two register operands (source, destination)
- **Format D**: Register + immediate value
- **Format E**: Wide immediate (24-bit or 32-bit)
- **Format F**: Memory addressing (base register + offset)
- **Format G**: Variable-length operands (strings, jump tables, raw bytes)

### Unified Interpreter Pattern
```python
def execute(bytecode):
    while ip < len(bytecode):
        opcode = bytecode[ip]
        format_family = decode_format(opcode)
        operands = extract_operands(format_family, bytecode, ip)
        result = dispatch(opcode, operands)
        ip += instruction_size(format_family, operands)
```

### Conformance Testing
- Generate test vectors independently of any runtime
- Each vector: input bytecode, expected final state (registers, memory, flags)
- Run vectors against ALL runtime implementations
- 100% pass rate = convergence achieved

### Escape Mechanism (0xFF)
- One opcode reserved as escape to extension space
- Next byte(s) identify the extension opcode
- Enables 253 base opcodes + 65,536 extension opcodes
- Must handle both valid and invalid extension opcodes gracefully

## Common Pitfalls
1. **Off-by-one in operand extraction**: Format G variable-length operands are the #1 source of bugs
2. **Missing bounds checks**: Always validate bytecode buffer bounds before reading operands
3. **Sign extension errors**: When widening values (8-bit to 32-bit), two's complement must be preserved
4. **Format decoding ambiguity**: Ensure format family detection is unambiguous for all opcodes
5. **Endianness**: Pick one (typically little-endian for x86) and document it

## Transferable Patterns
- The format-family pattern works for ANY instruction set (not just FLUX)
- Conformance testing approach applies to any multi-runtime project
- The escape mechanism is how x86, ARM, and other ISAs handle extension opcodes
- Unified interpreter pattern is how most modern VMs work (JVM, Python, etc.)

## References
- FLUX ISA v3 Specification: `docs/isa-v3-full-draft.md` (in flux-runtime repo)
- Conformance Test Vectors: `tools/conformance_generator.py` (221 vectors)
- Unified Interpreter: `src/flux/vm/unified_interpreter.py` (470 lines)
