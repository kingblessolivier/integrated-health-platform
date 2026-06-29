# Mobile — Integrated National Health Platform (Flutter)

Offline-first skeleton for the CHW, patient, and ambulance apps
(docs [51](../docs/51-mobile-offline-architecture.md), [28](../docs/28-mobile-sync-and-conflict-resolution.md)).

## Layout
```
lib/
  main.dart                    app entry
  core/theme.dart              design tokens (docs/05, Dart side)
  data/local/op_log.dart       offline operation-log (sync unit)
  data/sync/sync_engine.dart   idempotent replay + conflict handling
```

## Run
```bash
flutter pub get
flutter run
```

Local storage uses drift (SQLite) + Hive; encrypt with SQLCipher and pin TLS certs in
production (docs/39). iCCM trees and the GPS polygon check run on-device, offline.
