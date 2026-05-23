package com.utilityclient.client.util;

import net.minecraft.client.player.LocalPlayer;
import net.minecraft.world.entity.Entity;

public final class MovementUtil {
    private MovementUtil() {
    }

    public static double horizontalSpeed(Entity entity) {
        double dx = entity.getX() - entity.xOld;
        double dz = entity.getZ() - entity.zOld;
        return Math.sqrt(dx * dx + dz * dz) * 20.0D;
    }

    public static double verticalSpeed(Entity entity) {
        return (entity.getY() - entity.yOld) * 20.0D;
    }

    public static MovementMode mode(LocalPlayer player) {
        if (player.getVehicle() != null) {
            String id = player.getVehicle().getType().toString().toLowerCase();
            if (id.contains("zombie_nautilus")) {
                return MovementMode.ZOMBIE_NAUTILUS;
            }
            if (id.contains("nautilus")) {
                return MovementMode.NAUTILUS;
            }
            if (id.contains("camel_husk")) {
                return MovementMode.CAMEL_HUSK;
            }
            if (id.contains("camel")) {
                return MovementMode.CAMEL;
            }
            if (id.contains("zombie_horse")) {
                return MovementMode.ZOMBIE_HORSE;
            }
            return MovementMode.HORSE;
        }
        if (player.isFallFlying()) {
            return MovementMode.ELYTRA;
        }
        if (player.isSwimming()) {
            return MovementMode.SWIMMING;
        }
        if (player.isSprinting()) {
            return MovementMode.SPRINTING;
        }
        return MovementMode.WALKING;
    }
}
