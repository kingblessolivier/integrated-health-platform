/// Ray-casting point-in-polygon test. Mirrors the server's `point_in_polygon`
/// (backend/apps/community/services.py) so the GPS village-polygon check agrees on
/// device and server. Runs fully offline (docs/51).
///
/// `point` is (lng, lat); `polygon` is a list of (lng, lat) vertices.
bool pointInPolygon((double, double) point, List<(double, double)> polygon) {
  if (polygon.length < 3) return false;
  final x = point.$1, y = point.$2;
  var inside = false;
  var j = polygon.length - 1;
  for (var i = 0; i < polygon.length; i++) {
    final xi = polygon[i].$1, yi = polygon[i].$2;
    final xj = polygon[j].$1, yj = polygon[j].$2;
    final intersects =
        ((yi > y) != (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
    if (intersects) inside = !inside;
    j = i;
  }
  return inside;
}
