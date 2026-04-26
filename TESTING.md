# TESTING – SeeBus‑Global

This document describes how to test the SeeBus‑Global backend.  
All tests are manual, deterministic, and do not require internet access except for GTFS‑RT validation.

---------------------------------------

## 1. Test Categories

The project uses the following test groups:

1. Basic functionality tests  
2. Error‑state tests  
3. Input‑validation tests  
4. Security constraint tests  
5. Filesystem safety tests  
6. GTFS static data tests  
7. GTFS‑RT real‑time tests  
8. ETA engine tests  
9. Event engine tests  
10. API endpoint tests  

Each test must be reproducible and independent.

---------------------------------------

## 2. Basic Functionality Tests

### 2.1 Start the backend
Command:
python main.py

Expected:
- Server starts without errors  
- Static GTFS loads successfully  
- Status endpoint returns OK  

### 2.2 Status endpoint
curl http://localhost:8080/status

Expected:
{ "status": "ok" }

---------------------------------------

## 3. Error‑State Tests

### 3.1 Missing GTFS files
Remove one GTFS file (e.g., stops.txt).

Expected:
- Server refuses to start  
- Clear error message  

### 3.2 Invalid YAML
Break config.yaml formatting.

Expected:
- Server refuses to start  
- Error: invalid configuration  

### 3.3 Port already in use
Run two instances.

Expected:
- Second instance fails with port‑in‑use error  

---------------------------------------

## 4. Input‑Validation Tests

### 4.1 Invalid route
/api/eta?route=XYZ&stop_id=BB1001

Expected:
- error: true  
- code: INVALID_REQUEST  

### 4.2 Invalid stop
/api/eta?route=24&stop_id=INVALID

Expected:
- error: true  
- code: NOT_FOUND  

### 4.3 Missing parameters
/api/eta

Expected:
- error: true  
- message: missing parameters  

---------------------------------------

## 5. Security Constraint Tests

### 5.1 Directory traversal
/api/eta?route=../../etc/passwd

Expected:
- Request rejected  
- No filesystem access  

### 5.2 Oversized input
/api/eta?route=<10k characters>

Expected:
- Request rejected  
- No crash  

---------------------------------------

## 6. Filesystem Safety Tests

### 6.1 Read‑only GTFS directory
Set GTFS folder to read‑only.

Expected:
- Server still runs  
- No write attempts  

### 6.2 Log file rotation
Fill log file to large size.

Expected:
- No crash  
- Logging continues  

---------------------------------------

## 7. GTFS Static Data Tests

### 7.1 Stops loaded
Check internal cache.

Expected:
- All stops present  
- No duplicates  

### 7.2 Trips loaded
Expected:
- All trips have valid stop sequences  

---------------------------------------

## 8. GTFS‑RT Real‑Time Tests

### 8.1 Valid feed
Use real provider.

Expected:
- TripUpdates processed  
- VehiclePositions updated  

### 8.2 Invalid feed
Point GTFS_RT_URL to invalid URL.

Expected:
- Graceful fallback  
- No crash  

---------------------------------------

## 9. ETA Engine Tests

### 9.1 Static ETA
Disable GTFS‑RT.

Expected:
- ETA computed from schedule only  

### 9.2 Delayed trip
Inject delay in TripUpdate.

Expected:
- ETA reflects delay  

### 9.3 Cancelled trip
Inject cancellation.

Expected:
- status: "cancelled"  

---------------------------------------

## 10. Event Engine Tests

### 10.1 Arrival imminent
Simulate ETA < 120 seconds.

Expected:
- Event: ARRIVAL_IMMINENT  

### 10.2 At stop
Simulate vehicle position at stop.

Expected:
- Event: AT_STOP  

### 10.3 Approaching destination
Simulate last segment.

Expected:
- Event: APPROACHING_DESTINATION  

---------------------------------------

## 11. API Endpoint Tests

### 11.1 /journey
POST new journey.

Expected:
- journey_id returned  
- state: initialized  

### 11.2 /journey/{id}
Expected:
- correct state  
- correct next_stop  

### 11.3 /events/{id}
Expected:
- list of events  
- timestamps valid  

---------------------------------------

## 12. Load Testing (Optional)

### 12.1 1000 ETA requests
Expected:
- No crashes  
- Response time < 50 ms  

### 12.2 Continuous 24‑hour run
Expected:
- No memory leaks  
- Stable performance  

---------------------------------------

# End of file

