# Utility Client

Utility Client is a purely client-side Fabric mod scaffold for Minecraft Java Edition `1.21.11` ("Mounts of Mayhem").

## Build Notes

- Minecraft: `1.21.11`
- Java: `21`
- Loader: Fabric
- Mappings: official Mojang mappings through Loom
- Loom plugin: `net.fabricmc.fabric-loom-remap`
- Current scaffolded Loom version: `1.14.3`

## Build

1. Install Java 21.
2. Generate a Gradle wrapper with a local Gradle install by running `gradle wrapper`.
3. From this project directory, run `./gradlew build`.
4. Use `./gradlew runClient` for a dev client.

## Version Strategy

Minecraft `1.21.11` is the last obfuscated Java Edition release. This project uses `loom.officialMojangMappings()` so the codebase stays aligned with Fabric's migration path toward post-`1.21.11` unobfuscated versions.

## Scope

This scaffold includes:

- Core module architecture
- JSON config persistence
- HUD editor and click GUI foundations
- Showcase mount HUD module for 1.21.11-specific mounts and armor
- Initial implementations for the requested Lunar-style utility modules

Some advanced systems such as chunk-color minimap rendering, full fog-of-war world maps, and deep render/input internals are scaffolded in a conservative way so the project remains maintainable and can be iterated safely against real 1.21.11 runtime mappings.
