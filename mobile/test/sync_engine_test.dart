import 'package:flutter_test/flutter_test.dart';
import 'package:inhp_mobile/data/local/op_log.dart';
import 'package:inhp_mobile/data/sync/sync_engine.dart';

Op _visit(String id) => Op(
      clientOpId: id,
      entityType: 'chw_visit',
      entityId: 'enc-1',
      opType: 'create',
      command: 'CHIC',
      patch: const {'kind': 'iccm'},
    );

void main() {
  test('successful push marks the op synced', () async {
    final dao = InMemoryOpLogDao();
    await dao.append(_visit('1'));
    await SyncEngine(opLog: dao, push: (op) async => 201).syncPending();
    expect(dao.all.single.status, OpStatus.synced);
  });

  test('409 marks the op as a conflict (no silent overwrite)', () async {
    final dao = InMemoryOpLogDao();
    await dao.append(_visit('1'));
    await SyncEngine(opLog: dao, push: (op) async => 409).syncPending();
    expect(dao.all.single.status, OpStatus.conflict);
  });

  test('network error leaves the op pending for retry', () async {
    final dao = InMemoryOpLogDao();
    await dao.append(_visit('1'));
    await SyncEngine(opLog: dao, push: (op) async => 0).syncPending();
    expect(dao.all.single.status, OpStatus.pending);
  });

  test('a synced op is not pushed again (idempotent replay)', () async {
    final dao = InMemoryOpLogDao();
    await dao.append(_visit('1'));
    var calls = 0;
    final engine = SyncEngine(opLog: dao, push: (op) async {
      calls++;
      return 201;
    });
    await engine.syncPending();
    await engine.syncPending();
    expect(calls, 1);
  });
}
