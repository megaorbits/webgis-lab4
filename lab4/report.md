# Lab 4 Report — GeoDjango with PostGIS, admin and Leaflet

**Name:** Muhammad Ahmad  
**Roll no.:** 538160  
**Course:** WebGIS  
**Project folder:** `C:\webgis-lab`  
**Repository:** https://github.com/megaorbits/webgis-lab4

This lab builds a Django + PostGIS backend and a Leaflet map of Pakistan’s districts. The map is served from the database, not from a static GeoJSON file. Clicking the map asks PostGIS which district contains the point.

There is no live public URL. GitHub Pages cannot run Python or PostgreSQL. The app runs locally at `http://127.0.0.1:8000/`.

---

## 1. Checkpoint screenshots

Screenshots are included in the order of the numbered files in each checkpoint folder. There is no `checkpoint1` folder in the project; Checkpoint 2 is the first captured set.

### Checkpoint 2 — OSGeo4W, settings, and PostGIS

**2.1** OSGeo4W / GDAL on this machine. The lab path `C:\OSGeo4W\bin` is not used here. GDAL is installed at `%LOCALAPPDATA%\Programs\OSGeo4W`. `gdalinfo --version` reports **GDAL 3.13.3 "Iowa City"**.

![Checkpoint 2 screenshot 1: OSGeo4W GDAL path](../checkpoint2/confirming%20the%20isntallation%20and%20path%20of%20osgeo%201.png)

**2.2** `webgis/settings.py`: `django.contrib.gis` and `districts` are installed. The database engine is PostGIS. The password is read from `WEBGIS_DB_PASSWORD`, not written in the file.

![Checkpoint 2 screenshot 2: settings.py database and GIS apps](../checkpoint2/editing%20settings.py%202.png)

**2.3** PostGIS enabled on the `webgis` database in pgAdmin (`CREATE EXTENSION postgis;`). The message `extension "postgis" already exists` means the extension was already installed.

![Checkpoint 2 screenshot 3: CREATE EXTENSION postgis](../checkpoint2/setup%20the%20postgis%20inside%20postgres%203.png)

**2.4** `SELECT postgis_full_version();` after Django tables appear in the `webgis` schema (PostGIS **3.6.2**, PostgreSQL **18**).

![Checkpoint 2 screenshot 4: PostGIS full version after Django tables](../checkpoint2/verifying%20django%20migrations%204.png)

### Checkpoint 3 — Database connection and migrate

**3.1** First connection failed with `fe_sendauth: no password supplied` because `WEBGIS_DB_PASSWORD` was not set in that terminal. After the variable was set, `Database connection: SUCCESS`, then `python manage.py migrate` applied Django’s built-in migrations.

![Checkpoint 3 screenshot 1: password error then successful migrate](../checkpoint3/migration%20compelted%201.png)

**3.2** PostGIS version confirmed again in pgAdmin on database `webgis`.

![Checkpoint 3 screenshot 2: postgis_full_version](../checkpoint3/postgis%20full%20version%202.png)

### Checkpoint 4 — District model and GiST index

**4.1** `District` model with `name` and `geom = MultiPolygonField(srid=4326)`. `makemigrations districts` created `0001_initial.py`. `sqlmigrate districts 0001` shows `CREATE TABLE "districts_district"` and `CREATE INDEX ... USING GIST ("geom")`.

![Checkpoint 4 screenshot 1: sqlmigrate GiST index](../checkpoint4/created%20database%20table%201.png)

**4.2** pgAdmin: table `districts_district` with columns `id`, `name`, `geom` (geometry MultiPolygon, 4326).

![Checkpoint 4 screenshot 2: districts_district columns](../checkpoint4/verifying%20colomns%20in%20postgres%202.png)

### Checkpoint 5 — Load 160 districts

**5.1** Source file present: `data/districts.geojson`.

![Checkpoint 5 screenshot 1: dir data](../checkpoint5/dir%20data%201.png)

**5.2** First load attempt used `from districts import load` and failed with `ImportError: cannot import name 'load'`. After `load.py` was in place, the loader ran: **160 features**, **160 districts saved**.

![Checkpoint 5 screenshot 2: load.py ImportError then 160 districts](../checkpoint5/loading%20successful%202.png)

**5.3** Extra fields (`province`, `pcode`, `pop_2023`, `area_km2`) added as nullable columns. `makemigrations` / `migrate` applied `0002_...`.

![Checkpoint 5 screenshot 3: migration 0002 extra fields](../checkpoint5/migrations%20again%20for%20province%203.png)

**5.4** Django shell checks: 160 districts; 29 in Sindh; 25 with `pop_2023` null; Lahore population and `MultiPolygon` geometry.

![Checkpoint 5 screenshot 4: shell counts and Lahore](../checkpoint5/testing%20different%20commands%204.png)

### Checkpoint 6 — Django admin

**6.1** Django admin at `/admin/` with the Districts app registered (user **AHMAD**).

![Checkpoint 6 screenshot 1: Django administration](../checkpoint6/django%20administration%201.png)

**6.2** Lahore geometry on the admin map (OpenStreetMap), with an extra vertex used for the database-edit exercise.

![Checkpoint 6 screenshot 2: Lahore admin map](../checkpoint6/lahore%202.png)

**6.3** Change-district form for Lahore: province Punjab, pcode PK617, pop_2023 **13004135**, area 1729.9 km².

![Checkpoint 6 screenshot 3: Lahore admin form](../checkpoint6/lahore%203.png)

**6.4** pgAdmin confirms the edited population:

```sql
SELECT name, pop_2023 FROM districts_district WHERE name = 'Lahore';
```

Result: Lahore, **13004135**.

![Checkpoint 6 screenshot 4: SQL confirms Lahore pop_2023](../checkpoint6/query%20run%20success%204.png)

### Checkpoint 7 — Leaflet map from the Django API

**7.1** Map of 160 districts, coloured by province. DevTools Network shows `GET /api/districts/` → **200 OK**, `Content-Type: application/geo+json`, `Content-Length: 1026495`.

![Checkpoint 7 screenshot 1: map and Network tab for api/districts](../checkpoint7/districtd%20maps%20with%20network%201.png)

**7.2** Full map view: OSM/Esri topo basemap and province-coloured polygons (Punjab green, Sindh orange, Balochistan magenta, KP purple, Gilgit-Baltistan brown, Azad Kashmir gold).

![Checkpoint 7 screenshot 2: classified district map](../checkpoint7/json%20api7%20start%202.png)

### Checkpoint 8 / 9 — Spatial question (bonus)

There is no separate `checkpoint8` folder. The Part 8 extension screenshots are in `checkpoint 9`, numbered 1 then 2.

**9.1** Map click / hover lookup: **Islamabad, Islamabad**. The `/api/where/?lat=...&lng=...` view uses `geom__contains` on a `Point(lng, lat, srid=4326)`.

![Checkpoint 9 screenshot 1: Islamabad spatial lookup](../checkpoint%209/bonus%201.png)

**9.2** Area comparison query for Lahore, Gilgit and Gwadar (see table in section 4).

![Checkpoint 9 screenshot 2: stored vs geodesic vs Web Mercator area](../checkpoint%209/bonus%202.png)

---

## 2. Software versions

| Software | Version on this machine |
|---|---|
| Python | 3.15.0 (64-bit) |
| Django | 6.1.2 |
| PostgreSQL | 18.6 (`PostgreSQL 18.6 on x86_64-windows`) |
| PostGIS | 3.6.2 |
| GDAL | 3.13.3 "Iowa City" (2026/08/13) |
| GEOS (from PostGIS) | 3.14.1dev-CAPI-1.20.4 |
| PROJ (from PostGIS) | 8.2.1 |
| psycopg | 3.3.6 |

OSGeo4W is installed at `%LOCALAPPDATA%\Programs\OSGeo4W`, not `C:\OSGeo4W`. `webgis/settings.py` points GeoDjango at that location.

---

## 3. Installation errors and fixes

Several problems did occur. The messages below are copied from the checkpoint terminals and from later debugging.

### 3.1 OSGeo4W path not `C:\OSGeo4W`

**Symptom (Checkpoint 2.1):**

```text
The system cannot find the path specified.
'bin' is not recognized as an internal or external command,
operable program or batch file.
```

**Cause:** The lab assumes `C:\OSGeo4W`. This PC installed OSGeo4W under `%LOCALAPPDATA%\Programs\OSGeo4W`.

**Fix:** Use that path. Confirm with:

```text
gdalinfo --version
GDAL 3.13.3 "Iowa City", released 2026/08/13
```

`settings.py` sets `OSGEO4W_ROOT`, `GDAL_DATA`, `PROJ_LIB` and prepends `...\OSGeo4W\bin` to `PATH`.

### 3.2 `fe_sendauth: no password supplied`

**Symptom (Checkpoint 3.1):**

```text
django.db.utils.OperationalError: connection to server at "127.0.0.1", port 5432 failed: fe_sendauth: no password supplied
Multiple connection attempts failed. All failures were:
- host: 'localhost', port: '5432', hostaddr: '::1': connection failed: connection to server at "::1", port 5432 failed: fe_sendauth: no password supplied
- host: 'localhost', port: '5432', hostaddr: '127.0.0.1': connection failed: connection to server at "127.0.0.1", port 5432 failed: fe_sendauth: no password supplied
```

**Cause:** `WEBGIS_DB_PASSWORD` was not set in that PowerShell window.

**Fix:** Set the environment variable (no password is stored in the repo), reopen the terminal, then:

```text
Database connection: SUCCESS
python manage.py migrate
```

Migrations then applied (`auth`, `admin`, `contenttypes`, `sessions`).

### 3.3 `CREATE EXTENSION postgis` already exists

**Symptom (Checkpoint 2.3):**

```text
ERROR:  extension "postgis" already exists
SQL state: 42710
```

**Cause:** PostGIS was already enabled on `webgis`.

**Fix:** None required. `SELECT postgis_full_version();` succeeded.

### 3.4 Cannot import `load`

**Symptom (Checkpoint 5.2):**

```text
ImportError: cannot import name 'load' from 'districts' (C:\webgis-lab\districts\__init__.py)
```

**Cause:** `python manage.py shell -c "from districts import load; load.run()"` was run before `districts/load.py` was available as an importable module (or from a broken first attempt).

**Fix:** Ensure `districts/load.py` exists, then run the same command again. Output:

```text
districts : 160 features, Unknown geometry
160 districts saved
```

### 3.5 Non-nullable field on makemigrations

**Symptom (Checkpoint 5.3):**

```text
It is impossible to add a non-nullable field 'pcode' to district without specifying a default.
```

**Cause:** Rows already existed from the first load; a new required column needs a default.

**Fix:** Fields were defined with `null=True, blank=True`, then `makemigrations` / `migrate` created `0002_district_area_km2_district_pcode_district_pop_2023_and_more`.

### 3.6 `TemplateDoesNotExist: districts/map.html`

**Symptom (Part 7):** Django could not find the map template.

**Cause:** The template was not at `districts/templates/districts/map.html`.

**Fix:** Place the file at that path (`APP_DIRS` is True and `districts` is in `INSTALLED_APPS`).

### 3.7 `NoReverseMatch` for `district-at`

**Symptom:** The map template called `{% url 'district-at' %}` before Part 8 existed, so the page could not render and polygons did not load.

**Fix:** Keep the Part 7 GeoJSON URL, and add `path("api/where/", views.district_at, name="district-at")` plus the `district_at` view in Part 8.

---

## 4. Area table from Part 8

Query:

```sql
SELECT
    name,
    ROUND(area_km2) AS stored,
    ROUND((ST_Area(geom::geography) / 1e6)::numeric) AS geodesic,
    ROUND((ST_Area(ST_Transform(geom, 3857)) / 1e6)::numeric) AS web_mercator
FROM districts_district
WHERE name IN ('Lahore', 'Gilgit', 'Gwadar');
```

| name | stored (km²) | geodesic (km²) | web_mercator (km²) |
|---|---:|---:|---:|
| Gwadar | 11574 | 11574 | 14244 |
| Gilgit | 4016 | 4015 | 6133 |
| Lahore | 1730 | 1730 | 2385 |

Stored areas match the geodesic (spheroid) calculation closely. Web Mercator (EPSG:3857) inflates area, more so for Gilgit at higher latitude, because that projection stretches east–west as you move away from the equator.

---

## 5. Answers to the questions

### 1. What can a Django + PostGIS page do instead of sending the whole GeoJSON file?

In Labs 2 and 3 the browser downloaded every district. Here the server can query PostGIS and return only what the page needs. Two examples from this lab:

1. **Attribute filter:** `GET /api/districts/?province=Sindh` runs `District.objects.filter(province=province)` and returns 29 Sindh features instead of all 160.
2. **Spatial filter:** `GET /api/where/?lat=33.6423&lng=72.9906` builds a point and uses `geom__contains`, returning one JSON object (`Islamabad`) instead of the full polygon dataset.

### 2. Why is the database password an environment variable?

If the password were written in `settings.py`, it would be copied into Git and into any zip or LMS upload. Anyone with the repo could log in as `postgres`. `os.environ.get("WEBGIS_DB_PASSWORD")` keeps the secret on the local machine. This repository does not contain the password.

### 3. What does `USING GIST` do, and which query benefits?

GiST (Generalized Search Tree) is PostgreSQL’s spatial index type. The migration builds an index on `districts_district.geom`. PostGIS can then find candidate polygons by bounding box before running the exact `ST_Contains` test.

The query that benefits most is Part 8: `District.objects.filter(geom__contains=point)` / `ST_Contains(geom, point)` on every map click. Without the index, PostgreSQL would scan all 160 geometries for each click. Province filters on text columns use a normal (non-GiST) index if one exists; they do not use this geometry index.

### 4. Why wrap some geometries in a `MultiPolygon`?

`District.geom` is a `MultiPolygonField`. The GeoJSON mix includes both `Polygon` and `MultiPolygon`. GeoDjango will not save a `Polygon` into a `MultiPolygonField`; insert would raise a type error for those features and the load would stop short of 160 rows. Wrapping a single polygon as `MultiPolygon(geom, srid=4326)` matches the field type. Features that are already multipolygons are stored as they are.

### 5. Who should have an admin login?

**Should:** a small set of data stewards (for example a GIS officer, course instructor, or designated TA) who are allowed to correct names, population, or boundaries.

**Should not:** the public map audience, anonymous visitors, or every student who only needs to view the map. Admin can change and delete geometry. A public account would be a vandalism and privacy risk. If students must practise, they should get a limited account (change but not delete), not the `postgres`/superuser login.

### 6. `[lat, lng]` vs `(lng, lat)`, and the URL

- **Leaflet** uses `[lat, lng]`: `setView([30.3753, 69.3451], 5)` and `e.latlng.lat` / `e.latlng.lng` on click.
- **PostGIS / GeoDjango `Point`** uses `(lng, lat)`: `Point(lng, lat, srid=4326)` because GeoJSON and WKT are x, y (longitude, latitude).
- **The `/api/where/` URL** does not rely on argument order. It uses named parameters, `?lat=33.6423&lng=72.9906`. Django reads `request.GET["lat"]` and `request.GET["lng"]` by name, then constructs `Point(lng, lat)`. Swapping the query string to `?lng=72.9906&lat=33.6423` still works. Swapping the *values* (putting latitude into `lng`) would place the point in the wrong hemisphere.

---

## 6. What was submitted

- Django project `webgis` with app `districts`
- PostGIS database `webgis`, 160 districts loaded
- Admin for `District`
- Leaflet map from `/api/districts/`
- Part 8 extension: `/api/where/` plus the area SQL
- `lab4/.gitignore` (venv and bytecode not committed)
- This report

LMS submission: repository link https://github.com/megaorbits/webgis-lab4
