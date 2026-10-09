import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';

abstract class SyncState extends Equatable {
  final int pendingCount;
  final bool isOnline;

  const SyncState({
    required this.pendingCount,
    required this.isOnline,
  });

  @override
  List<Object?> get props => [pendingCount, isOnline];
}

class SyncIdle extends SyncState {
  const SyncIdle({required int pendingCount, required bool isOnline})
      : super(pendingCount: pendingCount, isOnline: isOnline);
}

class SyncInProgress extends SyncState {
  const SyncInProgress({required int pendingCount, required bool isOnline})
      : super(pendingCount: pendingCount, isOnline: isOnline);
}

class SyncOfflineState extends SyncState {
  const SyncOfflineState({required int pendingCount})
      : super(pendingCount: pendingCount, isOnline: false);
}

class SyncErrorState extends SyncState {
  final String errorMessage;
  const SyncErrorState({
    required int pendingCount,
    required bool isOnline,
    required this.errorMessage,
  }) : super(pendingCount: pendingCount, isOnline: isOnline);

  @override
  List<Object?> get props => [pendingCount, isOnline, errorMessage];
}

class SyncCubit extends Cubit<SyncState> {
  SyncCubit() : super(const SyncIdle(pendingCount: 0, isOnline: true));

  void updateConnectivity(bool online) {
    if (!online) {
      emit(SyncOfflineState(pendingCount: state.pendingCount));
    } else {
      emit(SyncIdle(pendingCount: state.pendingCount, isOnline: true));
    }
  }

  void updatePendingCount(int count) {
    if (!state.isOnline) {
      emit(SyncOfflineState(pendingCount: count));
    } else {
      emit(SyncIdle(pendingCount: count, isOnline: true));
    }
  }

  Future<void> syncNow(Future<void> Function() syncEngineTrigger) async {
    if (!state.isOnline) {
      emit(SyncOfflineState(pendingCount: state.pendingCount));
      return;
    }

    emit(SyncInProgress(pendingCount: state.pendingCount, isOnline: true));
    try {
      await syncEngineTrigger();
      emit(const SyncIdle(pendingCount: 0, isOnline: true));
    } catch (e) {
      emit(SyncErrorState(
        pendingCount: state.pendingCount,
        isOnline: true,
        errorMessage: e.toString(),
      ));
    }
  }
}
