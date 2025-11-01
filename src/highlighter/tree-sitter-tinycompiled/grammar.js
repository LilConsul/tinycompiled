/**
 * @file Tiny Compiled - Custom assembly-like language, designed to help new developers understand the fundamentals of assembly language
 * @author Shevchenko Denys
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: "tinycompiled",

  extras: $ => [
    /\s/,
    $.comment,
  ],

  rules: {
    source_file: $ => repeat($._statement),

    _statement: $ => choice(
      $.variable_declaration,
      $.data_movement,
      $.arithmetic_operation,
      $.logical_operation,
      $.shift_operation,
      $.function_definition,
      $.function_call,
      $.return_statement,
      $.loop_statement,
      $.while_statement,
      $.for_statement,
      $.repeat_statement,
      $.if_statement,
      $.stack_operation,
      $.io_operation,
      $.special_instruction,
      $.label,
      $.comment,
    ),

    // Comments
    comment: $ => token(seq(';', /.*/)),

    // Variable Declaration
    variable_declaration: $ => seq(
      'VAR',
      field('name', $.identifier),
      optional(seq(',', field('value', $._operand))),
    ),

    // Data Movement
    data_movement: $ => choice(
      // LOAD register, immediate/identifier
      seq(
        'LOAD',
        field('dest', $.register),
        ',',
        field('src', $._operand),
      ),
      // SET identifier, immediate/register
      seq(
        'SET',
        field('dest', $.identifier),
        ',',
        field('src', choice($.register, $.immediate)),
      ),
      // MOVE register, register
      seq(
        'MOVE',
        field('dest', $.register),
        ',',
        field('src', $.register),
      ),
    ),

    // Arithmetic Operations
    arithmetic_operation: $ => choice(
      // ADD/SUB/MUL/DIV register, register, register/immediate
      seq(
        field('op', choice('ADD', 'SUB', 'MUL', 'DIV')),
        field('dest', $.register),
        ',',
        field('src1', $.register),
        ',',
        field('src2', choice($.register, $.immediate)),
      ),
      // INC/DEC register/identifier
      seq(
        field('op', choice('INC', 'DEC')),
        field('target', choice($.register, $.identifier)),
      ),
    ),

    // Logical/Bitwise Operations
    logical_operation: $ => choice(
      // AND/OR/XOR register, register, register
      seq(
        field('op', choice('AND', 'OR', 'XOR')),
        field('dest', $.register),
        ',',
        field('src1', $.register),
        ',',
        field('src2', $.register),
      ),
      // NOT register
      seq(
        'NOT',
        field('target', $.register),
      ),
    ),

    // Shift Operations
    shift_operation: $ => seq(
      field('op', choice('SHL', 'SHR')),
      field('dest', $.register),
      ',',
      field('src', $.register),
      ',',
      field('count', $.immediate),
    ),

    // Function Definition
    function_definition: $ => seq(
      'FUNC',
      field('name', $.identifier),
      repeat($._statement),
      'ENDFUNC',
    ),

    // Function Call
    function_call: $ => seq(
      'CALL',
      field('name', $.identifier),
    ),

    // Return Statement
    return_statement: $ => seq(
      'RET',
      optional(field('value', $.register)),
    ),

    // Loop Statement
    loop_statement: $ => seq(
      'LOOP',
      field('counter', $.identifier),
      ',',
      field('limit', $.immediate),
      repeat($._statement),
      'ENDLOOP',
    ),

    // While Statement
    while_statement: $ => seq(
      'WHILE',
      field('condition', $.condition),
      repeat($._statement),
      'ENDWHILE',
    ),

    // For Statement
    for_statement: $ => seq(
      'FOR',
      field('variable', $.identifier),
      'FROM',
      field('start', $.immediate),
      'TO',
      field('end', $.immediate),
      optional(seq('STEP', field('step', $.immediate))),
      repeat($._statement),
      'ENDFOR',
    ),

    // Repeat-Until Statement
    repeat_statement: $ => seq(
      'REPEAT',
      repeat($._statement),
      'UNTIL',
      field('condition', $.condition),
    ),

    // If Statement
    if_statement: $ => seq(
      'IF',
      field('condition', $.condition),
      repeat($._statement),
      optional(seq(
        'ELSE',
        repeat($._statement),
      )),
      'ENDIF',
    ),

    // Condition
    condition: $ => seq(
      field('left', choice($.register, $.identifier)),
      field('operator', choice('==', '!=', '>', '<', '>=', '<=')),
      field('right', choice($.register, $.identifier, $.immediate)),
    ),

    // Stack Operations
    stack_operation: $ => choice(
      seq('PUSH', field('src', $.register)),
      seq('POP', field('dest', $.register)),
    ),

    // I/O Operations
    io_operation: $ => choice(
      // PRINT register/identifier/immediate
      seq(
        'PRINT',
        field('value', $._operand),
      ),
      // INPUT register/identifier
      seq(
        'INPUT',
        field('target', choice($.register, $.identifier)),
      ),
    ),

    // Special Instructions
    special_instruction: $ => choice(
      'HALT',
      'NOP',
    ),

    // Label
    label: $ => seq(
      field('name', $.identifier),
      ':',
    ),

    // Operand (immediate or identifier)
    _operand: $ => choice(
      $.immediate,
      $.identifier,
    ),

    // Register: R1-R8
    register: $ => /R[1-8]/,

    // Identifier: letters, digits, underscore (must start with letter/underscore)
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_]*/,

    // Immediate: decimal, hex, or binary
    immediate: $ => choice(
      /-?[0-9]+/,              // Decimal (including negative)
      /0x[0-9a-fA-F]+/,        // Hexadecimal
      /0b[01]+/,               // Binary
    ),
  }
});
