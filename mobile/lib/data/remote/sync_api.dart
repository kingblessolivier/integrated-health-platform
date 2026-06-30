import 'dart:convert';
import 'dart:io';

import '../local/op_log.dart';

/// Concrete sync push: POSTs an op to the API with the `Idempotency-Key` header so replays
/// are safe (docs/49, docs/51). Returns the HTTP status code (0 on network error → the
/// SyncEngine keeps the op pending for retry). Uses dart:io to avoid extra dependencies.
class SyncApi {
  SyncApi({required this.baseUrl, this.token});

  final String baseUrl; // e.g. https://api.example.rw/api/v1
  final String? token;

  Future<int> push(Op op) async {
    final client = HttpClient();
    try {
      final request = await client.postUrl(Uri.parse('$baseUrl/${_pathFor(op)}'));
      request.headers.contentType = ContentType.json;
      request.headers.set('Idempotency-Key', op.clientOpId);
      final t = token;
      if (t != null) request.headers.set('Authorization', 'Bearer $t');
      request.add(utf8.encode(jsonEncode(op.patch)));
      final response = await request.close();
      await response.drain<void>();
      return response.statusCode;
    } on Exception {
      return 0; // offline / network error — retryable
    } finally {
      client.close(force: true);
    }
  }

  String _pathFor(Op op) {
    switch (op.entityType) {
      case 'chw_visit':
        return 'chw-visits/';
      case 'referral':
        return 'referrals/';
      default:
        return '${op.entityType}s/';
    }
  }
}
