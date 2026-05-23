package com.utilityclient.client.gui;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.waypoint.Waypoint;
import net.minecraft.client.Minecraft;
import net.minecraft.client.input.MouseButtonEvent;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.core.BlockPos;
import net.minecraft.network.chat.Component;

public final class WorldMapScreen extends Screen {
    private double zoom = 1.0D;
    private double offsetX;
    private double offsetZ;

    public WorldMapScreen() {
        super(Component.literal("World Map"));
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, width, height, 0xC0101010);
        graphics.fill(30, 30, width - 30, height - 30, 0xCC111827);
        graphics.drawCenteredString(font, title, width / 2, 40, 0xFFFFFFFF);

        Minecraft client = Minecraft.getInstance();
        if (client.player != null) {
            BlockPos pos = client.player.blockPosition();
            graphics.drawString(font, "Center: " + pos.getX() + ", " + pos.getZ(), 40, 60, 0xFF93C5FD);
            graphics.drawString(font, "Zoom: " + String.format("%.2f", zoom), 40, 74, 0xFF93C5FD);
        }

        int markerY = 100;
        for (Waypoint waypoint : UtilityClientClient.waypointManager.getWaypoints()) {
            graphics.drawString(font, "- " + waypoint.name() + " [" + waypoint.x() + ", " + waypoint.z() + "]", 40, markerY, waypoint.color());
            markerY += 12;
            if (markerY > height - 50) {
                break;
            }
        }

        super.render(graphics, mouseX, mouseY, partialTick);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        zoom = Math.max(0.25D, Math.min(6.0D, zoom + scrollY * 0.1D));
        return true;
    }

    public boolean mouseDragged(MouseButtonEvent event, double dragX, double dragY) {
        offsetX += dragX;
        offsetZ += dragY;
        return true;
    }

    @Override
    public boolean mouseClicked(MouseButtonEvent event, boolean doubleClick) {
        Minecraft client = Minecraft.getInstance();
        if (client.player != null && event.button() == 1) {
            BlockPos pos = client.player.blockPosition();
            UtilityClientClient.waypointManager.add(new Waypoint(
                "Waypoint " + (UtilityClientClient.waypointManager.getWaypoints().size() + 1),
                pos.getX(),
                pos.getY(),
                pos.getZ(),
                0xFF10B981,
                client.player.level().dimension().identifier().toString(),
                true
            ));
            UtilityClientClient.configManager.saveAll();
            return true;
        }
        return super.mouseClicked(event, doubleClick);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}
