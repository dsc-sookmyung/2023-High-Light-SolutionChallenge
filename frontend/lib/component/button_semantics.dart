import 'package:flutter/widgets.dart';

class ButtonSemantics extends Semantics{
  ButtonSemantics({
    Key? key,
    String? label,
    Widget? child,
    bool excludeSemantics = false,
}) : super (
    key: key,
    label: label,
    child: child,
    excludeSemantics: excludeSemantics,
    button: true,
  );
}