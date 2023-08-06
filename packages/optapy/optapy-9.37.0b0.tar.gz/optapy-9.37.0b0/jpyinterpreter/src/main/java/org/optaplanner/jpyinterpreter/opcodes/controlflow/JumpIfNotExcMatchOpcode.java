package org.optaplanner.jpyinterpreter.opcodes.controlflow;

import java.util.List;
import java.util.Map;

import org.optaplanner.jpyinterpreter.FunctionMetadata;
import org.optaplanner.jpyinterpreter.PythonBytecodeInstruction;
import org.optaplanner.jpyinterpreter.StackMetadata;
import org.optaplanner.jpyinterpreter.implementors.JumpImplementor;

public class JumpIfNotExcMatchOpcode extends AbstractControlFlowOpcode {
    int jumpTarget;

    public JumpIfNotExcMatchOpcode(PythonBytecodeInstruction instruction, int jumpTarget) {
        super(instruction);
        this.jumpTarget = jumpTarget;
    }

    @Override
    public List<Integer> getPossibleNextBytecodeIndexList() {
        return List.of(
                getBytecodeIndex() + 1,
                jumpTarget);
    }

    @Override
    public void relabel(Map<Integer, Integer> originalBytecodeIndexToNewBytecodeIndex) {
        jumpTarget = originalBytecodeIndexToNewBytecodeIndex.get(jumpTarget);
        super.relabel(originalBytecodeIndexToNewBytecodeIndex);
    }

    @Override
    public List<StackMetadata> getStackMetadataAfterInstructionForBranches(FunctionMetadata functionMetadata,
            StackMetadata stackMetadata) {
        return List.of(stackMetadata.pop(2),
                stackMetadata.pop(2));
    }

    @Override
    public void implement(FunctionMetadata functionMetadata, StackMetadata stackMetadata) {
        JumpImplementor.popAndJumpIfExceptionDoesNotMatch(functionMetadata, stackMetadata, jumpTarget);
    }
}
