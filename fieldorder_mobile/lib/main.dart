import 'package:flutter/material.dart';
import 'app.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  // In production, initialize GetIt dependency injection and local Drift DB here
  runApp(const FieldOrderApp());
}
