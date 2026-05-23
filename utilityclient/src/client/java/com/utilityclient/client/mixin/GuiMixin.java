package com.utilityclient.client.mixin;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.module.misc.ScoreboardTweaksModule;
import net.minecraft.client.gui.Gui;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Gui.class)
public abstract class GuiMixin {

    /**
     * Cancels the scoreboard sidebar render when ScoreboardTweaks.hideEntirely is on.
     *
     * Method name "renderScoreboard" (Mojang mappings 1.20-1.21.x).
     * require = 0 prevents a hard crash if the name drifts in a future mapping update.
     */
    @Inject(method = "renderScoreboard", at = @At("HEAD"), cancellable = true, require = 0)
    private void utilityclient$maybeHideScoreboard(CallbackInfo ci) {
        if (UtilityClientClient.moduleManager == null) {
            return;
        }
        try {
            ScoreboardTweaksModule module = UtilityClientClient.moduleManager
                .getModuleByClass(ScoreboardTweaksModule.class);
            if (module.shouldHideEntirely()) {
                ci.cancel();
            }
        } catch (Exception ignored) {
        }
    }
}
