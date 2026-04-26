# CONFIGURATION – SeeBus‑Global

This document describes the configuration options for the SeeBus‑Global backend.
The configuration is designed to be simple, predictable, and suitable for local, staging, and production environments.

---------------------------------------

## 1. Environment Variables

The backend uses the following environment variables:

SEEBUS_PORT  
Port on which the API server runs.  
Example: 8080

GTFS_STATIC_PATH  
Path to static GTFS files (routes.txt, stops.txt, trips.txt…).  
Example: ./data/gtfs_static/

GTFS_RT_URL  
URL of the GTFS‑RT feed (TripUpdates, VehiclePositions).  
Example: https://transit.example.com/gtfs-rt/tripupdates

CACHE_TTL_SECONDS  
Time in seconds for which GTFS data should be cached in memory.  
Example: 30

ANNOUNCEMENTS_LANGUAGE  
Default language for announcements.  
Example: en

ANNOUNCEMENTS_VERBOSITY  
Announcement detail level (low | medium | high).  
Example: medium

ENABLE_TTS  
Enables or disables the TTS adapter (true | false).  
Example: true

---------------------------------------

## 2. Configuration File (config.yaml)

The project also supports YAML configuration:

server:
  port: 8080

gtfs:
  static_path: "./data/gtfs_static/"
  rt_url: "https://transit.example.com/gtfs-rt/tripupdates"
  cache_ttl: 30

announcements:
  language: "en"
  verbosity: "medium"
  tts_enabled: true

logging:
  level: "info"
  file: "./logs/seebus.log"

---------------------------------------

## 3. Configuration Priority

Configuration values are loaded in this order:

1. Environment variables  
2. config.yaml  
3. Default values in code  

Higher levels override lower ones.

---------------------------------------

## 4. Logging

The system supports three logging levels:

- error  
- info  
- debug  

Logs are written to the file defined in config.yaml.

---------------------------------------

## 5. Deployment Modes

LOCAL  
- static GTFS files from disk  
- TTS disabled  
- debug logs enabled

STAGING  
- GTFS‑RT from test feed  
- TTS optional  
- info logs

PRODUCTION  
- GTFS‑RT from production feed  
- TTS enabled  
- optimized caching and performance

---------------------------------------

## 6. Configuration Validation

On startup, the backend validates:

- existence of static GTFS files  
- availability of GTFS‑RT URL  
- correctness of YAML format  
- validity of verbosity level  
- whether the port is available  

If something is missing, the server will not start.

---------------------------------------

## 7. Minimal Configuration Example

SEEBUS_PORT=8080  
GTFS_STATIC_PATH=./data/gtfs_static/  
GTFS_RT_URL=https://transit.example.com/gtfs-rt/tripupdates  

---------------------------------------

## 8. Full Configuration Example

SEEBUS_PORT=8080  
GTFS_STATIC_PATH=./data/gtfs_static/  
GTFS_RT_URL=https://transit.example.com/gtfs-rt/tripupdates  
CACHE_TTL_SECONDS=30  
ANNOUNCEMENTS_LANGUAGE=en  
ANNOUNCEMENTS_VERBOSITY=medium  
ENABLE_TTS=true  

---------------------------------------

## 9. Notes

- YAML and environment variables can be used together.  
- YAML is optional but recommended for production.  
- All paths may be relative or absolute.  
- Custom API keys may be added for TTS adapters if needed.

---------------------------------------

# End of file
