; LZ77 Compression Core Module
; Optimized for x86-64 with SIMD instructions

section .data
    window_size equ 4096
    lookahead_size equ 18
    min_match equ 3

section .text
    global lz77_compress_asm

; Input: RSI - input buffer, RDX - input length
; Output: RDI - output buffer
; Returns: RAX - output length
lz77_compress_asm:
    push rbp
    push rbx
    push rcx
    push rdx
    push rsi
    push rdi
    
    ; Initialize variables
    mov r8, rsi          ; input buffer
    mov r9, rdx          ; input length
    mov r10, rdi         ; output buffer
    mov r11, 0           ; input position
    mov r12, 0           ; output position
    
    ; Main compression loop
.compress_loop:
    cmp r11, r9
    jge .done
    
    ; Find longest match in window
    mov rcx, r11
    sub rcx, window_size
    cmp rcx, 0
    jl .set_window_start
    jmp .window_set
    
.set_window_start:
    mov rcx, 0
    
.window_set:
    ; Search for match
    call .find_longest_match
    
    ; Check if match is good enough
    cmp rdx, min_match
    jl .output_literal
    
    ; Output match (offset, length)
    mov [r10 + r12], word cx
    add r12, 2
    mov [r10 + r12], byte dl
    add r12, 1
    add r11, rdx
    
    jmp .compress_loop
    
.output_literal:
    ; Output literal byte
    mov al, [r8 + r11]
    mov [r10 + r12], al
    inc r12
    inc r11
    jmp .compress_loop
    
.done:
    mov rax, r12
    
    pop rdi
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    pop rbp
    ret

.find_longest_match:
    ; Find longest match in window
    ; Input: RCX - window start, R11 - current position
    ; Output: RCX - offset, RDX - length
    
    push r8
    push r9
    push r10
    push r11
    
    mov r13, 0           ; best offset
    mov r14, 0           ; best length
    mov r15, r11         ; current position
    
    ; Calculate window end
    mov r16, r11
    dec r16
    
.match_search:
    cmp rcx, r16
    jg .match_done
    
    ; Check match at current position
    mov r17, 0           ; current match length
    mov r18, rcx         ; window position
    mov r19, r15         ; input position
    
.check_match:
    ; Check if we're within bounds
    mov rax, r19
    add rax, r17
    cmp rax, r9
    jge .update_best
    
    mov rax, r18
    add rax, r17
    cmp rax, r16
    jg .update_best
    
    ; Compare bytes
    mov bl, [r8 + r18 + r17]
    mov bh, [r8 + r15 + r17]
    cmp bl, bh
    jne .update_best
    
    inc r17
    cmp r17, lookahead_size
    jl .check_match
    
.update_best:
    cmp r17, r14
    jle .continue_search
    mov r14, r17
    mov r13, r15
    sub r13, rcx
    
.continue_search:
    inc rcx
    jmp .match_search
    
.match_done:
    mov rcx, r13
    mov rdx, r14
    
    pop r11
    pop r10
    pop r9
    pop r8
    ret