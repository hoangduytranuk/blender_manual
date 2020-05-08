public class SettingsPanel extends SimpleToolWindowPanel {

    public SettingsPanel(Project project) {
        super(false, true);
        final ActionManager actionManager = ActionManager.getInstance();
        DefaultActionGroup actionGroup = new DefaultActionGroup("ACTION_GROUP", false);
        actionGroup.add(ActionManager.getInstance().getAction("deployAction"));
        ActionToolbar actionToolbar = actionManager.createActionToolbar("ACTION_TOOLBAR", actionGroup, true);
        actionToolbar.setOrientation(SwingConstants.HORIZONTAL);
        this.setToolbar(actionToolbar.getComponent());

        