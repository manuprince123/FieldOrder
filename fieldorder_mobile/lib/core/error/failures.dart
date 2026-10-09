import 'package:equatable/equatable.dart';

abstract class Failure extends Equatable {
  final String message;
  const Failure(this.message);

  @override
  List<Object?> get props => [message];
}

class ServerFailure extends Failure {
  final int? statusCode;
  const ServerFailure(String message, {this.statusCode}) : super(message);

  @override
  List<Object?> get props => [message, statusCode];
}

class CacheFailure extends Failure {
  const CacheFailure(String message) : super(message);
}

class NetworkFailure extends Failure {
  const NetworkFailure(String message) : super(message);
}

class StockConflictFailure extends Failure {
  final Map<String, dynamic> details;
  const StockConflictFailure(String message, this.details) : super(message);

  @override
  List<Object?> get props => [message, details];
}

class ValidationFailure extends Failure {
  const ValidationFailure(String message) : super(message);
}
