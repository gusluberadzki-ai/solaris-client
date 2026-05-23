package com.utilityclient.client.module.combat;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.IntegerSetting;
import java.util.concurrent.ThreadLocalRandom;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.item.ItemStack;

public final class AutoClickerModule extends Module {
    private final IntegerSetting minCps = addSetting(new IntegerSetting("minCPS", "Minimum click rate", 8, 1, 25));
    private final IntegerSetting maxCps = addSetting(new IntegerSetting("maxCPS", "Maximum click rate", 12, 1, 25));
    private final BooleanSetting leftClick = addSetting(new BooleanSetting("leftClick", "Autoclick attack", true));
    private final BooleanSetting rightClick = addSetting(new BooleanSetting("rightClick", "Autoclick use", false));
    private final BooleanSetting respectSpearCharge = addSetting(new BooleanSetting("respectSpearCharge", "Do not interrupt spear charge attacks", true));

    private long nextLeftClick;
    private long nextRightClick;

    public AutoClickerModule(KeyMapping keybind) {
        super("AutoClicker", "Held-button Gaussian autoclicker with spear awareness.", Category.COMBAT, keybind);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onTick(Minecraft client) {
        if (client.player == null || client.screen != null) {
            return;
        }
        long now = System.currentTimeMillis();
        if (leftClick.get() && client.options.keyAttack.isDown() && now >= nextLeftClick && !shouldRespectSpearCharge(client)) {
            if (client.gameMode != null && client.player != null && client.hitResult instanceof EntityHitResult entityHitResult) {
                client.gameMode.attack(client.player, entityHitResult.getEntity());
            }
            if (client.player != null) {
                client.player.swing(InteractionHand.MAIN_HAND);
            }
            nextLeftClick = now + delayMillis();
        }
        if (rightClick.get() && client.options.keyUse.isDown() && now >= nextRightClick && !shouldRespectSpearCharge(client)) {
            if (client.gameMode != null && client.player != null) {
                client.gameMode.useItem(client.player, InteractionHand.MAIN_HAND);
            }
            nextRightClick = now + delayMillis();
        }
    }

    private boolean shouldRespectSpearCharge(Minecraft client) {
        if (!respectSpearCharge.get() || client.player == null) {
            return false;
        }
        ItemStack stack = client.player.getMainHandItem();
        String id = stack.getItem().toString().toLowerCase();
        return id.contains("spear") && client.player.isUsingItem();
    }

    private long delayMillis() {
        int min = Math.min(minCps.get(), maxCps.get());
        int max = Math.max(minCps.get(), maxCps.get());
        double sample = ThreadLocalRandom.current().nextGaussian((min + max) / 2.0D, Math.max(0.35D, (max - min) / 4.0D));
        double cps = Math.max(min, Math.min(max, sample));
        return (long) (1000.0D / cps);
    }
}
