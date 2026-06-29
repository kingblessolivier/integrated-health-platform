import '../local/op_log.dart';

/// Pushes queued offline ops on reconnect with idempotent replay and conflict handling
/// (docs/51). Pull/cursor logic omitted for brevity.
class SyncEngine {
  final OpLogDao opLog;
  final Future<int> Function(Op op) push; // returns HTTP status

  SyncEngine({required this.opLog, required this.push});

  Future<void> syncPending() async {
    for (final op in await opLog.pending()) {
      await opLog.setStatus(op.clientOpId, OpStatus.syncing);
      final status = await push(op); // Idempotency-Key = op.clientOpId
      if (status == 200 || status == 201) {
        await opLog.setStatus(op.clientOpId, OpStatus.synced);
      } else if (status == 409) {
        // Version conflict → surface to user for resolution (never silent overwrite).
        await opLog.setStatus(op.clientOpId, OpStatus.conflict);
      } else {
        // 5xx / offline → leave pending for exponential backoff retry.
        await opLog.setStatus(op.clientOpId, OpStatus.pending);
      }
    }
  }
}
