package com.utilityclient.client.module.world;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.util.RenderUtil;
import com.utilityclient.client.waypoint.Waypoint;
import net.fabricmc.fabric.api.client.rendering.v1.world.WorldRenderContext;
import net.minecraft.client.Camera;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.renderer.rendertype.RenderTypes;
import net.minecraft.world.phys.Vec3;
import org.joml.Matrix4f;

public final class WaypointsModule extends HudModule {
    private final IntegerSetting fadeCutoff = addSetting(new IntegerSetting("distanceFadeCutoff", "Distance fade cutoff", 300, 50, 5000));

    public WaypointsModule(KeyMapping keybind) {
        super("Waypoints", "Waypoint labels and in-world beacon beams.", Category.WORLD, keybind, 410, 228);
        width = 180;
        height = 44;
        setEnabledSilently(true);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (!isVisible() || client.player == null) {
            return;
        }
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int y = getY() + 6;
        for (Waypoint waypoint : UtilityClientClient.waypointManager.getWaypoints()
                .stream().filter(Waypoint::enabled).limit(3).toList()) {
            double dist = client.player.distanceToSqr(waypoint.x(), waypoint.y(), waypoint.z());
            RenderUtil.text(graphics,
                waypoint.name() + " " + String.format("%.1fm", Math.sqrt(dist)),
                getX() + 6, y, waypoint.color());
            y += 12;
        }
    }

    @Override
    public void onWorldRender(WorldRenderContext context) {
        Minecraft client = Minecraft.getInstance();
        if (client.player == null || client.level == null) return;

        Camera camera = context.gameRenderer().getMainCamera();
        Vec3 camPos = camera.position();
        int cutoffSq = fadeCutoff.get() * fadeCutoff.get();

        for (Waypoint waypoint : UtilityClientClient.waypointManager.getWaypoints()) {
            if (!waypoint.enabled()) continue;
            double distSq = client.player.distanceToSqr(waypoint.x(), waypoint.y(), waypoint.z());
            if (distSq > cutoffSq) continue;

            // Relative position from camera to waypoint column base
            double dx = waypoint.x() + 0.5 - camPos.x;
            double dy = waypoint.y()       - camPos.y;
            double dz = waypoint.z() + 0.5 - camPos.z;

            float alpha = Math.max(0.15f, 1.0f - (float)(distSq / cutoffSq));
            int color = waypoint.color();
            float r = ((color >> 16) & 0xFF) / 255f;
            float g = ((color >> 8)  & 0xFF) / 255f;
            float b = (color         & 0xFF) / 255f;

            PoseStack poseStack = context.matrices();
            poseStack.pushPose();
            poseStack.translate(dx, dy, dz);

            Matrix4f matrix = poseStack.last().pose();

            // Draw a vertical line from waypoint Y to Y+255 using the lines render type.
            VertexConsumer lines = context.consumers().getBuffer(RenderTypes.LINES);
            lines.addVertex(matrix, 0f, 0f,   0f).setColor(r, g, b, alpha).setNormal(0, 1, 0);
            lines.addVertex(matrix, 0f, 255f, 0f).setColor(r, g, b, alpha).setNormal(0, 1, 0);

            poseStack.popPose();
        }
    }
}
