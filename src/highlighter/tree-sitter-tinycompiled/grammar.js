/**
 * @file Tiny Compiled - Custom assembly-like language, designed to help new developers understand the fundamentals of assembly language
 * @author Shevchenko Denys
 * @license MIT
 */

/// <reference types="tree-sitter-cli/dsl" />
// @ts-check

module.exports = grammar({
  name: "tinycompiled",

  rules: {
    // TODO: add the actual grammar rules
    source_file: $ => "hello"
  }
});
