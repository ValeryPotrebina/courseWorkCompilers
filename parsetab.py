
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINUSleftMULTDIVrightPOWnonassocUMINUSDIV FUNCTION LPAREN MINUS MULT NUMBER PLUS POW RPAREN VARexpression : expression PLUS expression\n                  | expression MINUS expression \n                  | expression MULT expression  \n                  | expression DIV expression   \n                  | expression POW expressionexpression : LPAREN expression RPARENexpression : VARexpression : NUMBERexpression : MINUS expression %prec UMINUSexpression : FUNCTION LPAREN expression RPAREN\n                  | FUNCTION VAR '
    
_lr_action_items = {'LPAREN':([0,2,3,6,7,8,9,10,11,14,],[3,3,3,14,3,3,3,3,3,3,]),'VAR':([0,2,3,6,7,8,9,10,11,14,],[4,4,4,15,4,4,4,4,4,4,]),'NUMBER':([0,2,3,7,8,9,10,11,14,],[5,5,5,5,5,5,5,5,5,]),'MINUS':([0,1,2,3,4,5,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,],[2,8,2,2,-7,-8,2,2,2,2,2,-9,8,2,-11,-1,-2,-3,-4,-5,-6,8,-10,]),'FUNCTION':([0,2,3,7,8,9,10,11,14,],[6,6,6,6,6,6,6,6,6,]),'$end':([1,4,5,12,15,16,17,18,19,20,21,23,],[0,-7,-8,-9,-11,-1,-2,-3,-4,-5,-6,-10,]),'PLUS':([1,4,5,12,13,15,16,17,18,19,20,21,22,23,],[7,-7,-8,-9,7,-11,-1,-2,-3,-4,-5,-6,7,-10,]),'MULT':([1,4,5,12,13,15,16,17,18,19,20,21,22,23,],[9,-7,-8,-9,9,-11,9,9,-3,-4,-5,-6,9,-10,]),'DIV':([1,4,5,12,13,15,16,17,18,19,20,21,22,23,],[10,-7,-8,-9,10,-11,10,10,-3,-4,-5,-6,10,-10,]),'POW':([1,4,5,12,13,15,16,17,18,19,20,21,22,23,],[11,-7,-8,-9,11,-11,11,11,11,11,11,-6,11,-10,]),'RPAREN':([4,5,12,13,15,16,17,18,19,20,21,22,23,],[-7,-8,-9,21,-11,-1,-2,-3,-4,-5,-6,23,-10,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,3,7,8,9,10,11,14,],[1,12,13,16,17,18,19,20,22,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS expression','expression',3,'p_calc','syncanalyser.py',29),
  ('expression -> expression MINUS expression','expression',3,'p_calc','syncanalyser.py',30),
  ('expression -> expression MULT expression','expression',3,'p_calc','syncanalyser.py',31),
  ('expression -> expression DIV expression','expression',3,'p_calc','syncanalyser.py',32),
  ('expression -> expression POW expression','expression',3,'p_calc','syncanalyser.py',33),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','syncanalyser.py',40),
  ('expression -> VAR','expression',1,'p_expression_var','syncanalyser.py',45),
  ('expression -> NUMBER','expression',1,'p_expression_num','syncanalyser.py',50),
  ('expression -> MINUS expression','expression',2,'p_expression_uminus','syncanalyser.py',55),
  ('expression -> FUNCTION LPAREN expression RPAREN','expression',4,'p_expression_function','syncanalyser.py',61),
  ('expression -> FUNCTION VAR','expression',2,'p_expression_function','syncanalyser.py',62),
]
