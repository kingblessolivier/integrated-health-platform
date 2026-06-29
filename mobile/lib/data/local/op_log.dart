/// Offline operation-log (docs/51). Every offline write is appended here, never applied
/// directly; the log is the unit of sync. `clientOpId` doubles as the API Idempotency-Key.
enum OpStatus { pending, syncing, synced, conflict }

class Op {
  final String clientOpId; // UUID
  final String entityType; // patient | encounter | dispense ...
  final String entityId;
  final String opType; // create | update | delete
  final int? baseVersion; // server version the change was based on
  final Map<String, dynamic> patch;
  final String command; // command code, e.g. RXDP
  final DateTime createdAt;
  OpStatus status;

  Op({
    required this.clientOpId,
    required this.entityType,
    required this.entityId,
    required this.opType,
    required this.command,
    required this.patch,
    this.baseVersion,
    DateTime? createdAt,
    this.status = OpStatus.pending,
  }) : createdAt = createdAt ?? DateTime.now();
}

/// Backed by a drift (SQLite) table in the real app; interface kept minimal for the skeleton.
abstract class OpLogDao {
  Future<void> append(Op op);
  Future<List<Op>> pending();
  Future<void> setStatus(String clientOpId, OpStatus status);
}
