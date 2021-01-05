/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.htran.titlecase;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JEditorPane;
import org.openide.awt.ActionID;
import org.openide.awt.ActionReference;
import org.openide.awt.ActionReferences;
import org.openide.awt.ActionRegistration;
import org.openide.util.NbBundle.Messages;
import org.w3c.dom.Node;

@ActionID(
        category = "Edit",
        id = "org.htran.titlecase.TitleCaseAction"
)
@ActionRegistration(
        iconBase = "org/htran/titlecase/icon_title_case_16x16.png",
        displayName = "#CTL_TitleCaseAction"
)
@ActionReferences({
    /*
    @ActionReference(path = "Menu/Edit", position = 100, separatorAfter = 150),
    @ActionReference(path = "Toolbars/File", position = 0)
     */
    @ActionReference(path = "Menu/Edit", position = 100, separatorAfter = 150),
    @ActionReference(path = "Toolbars/Edit", position = 0),
    @ActionReference(path = "Editors/Popup")

})
@Messages("CTL_TitleCaseAction=Title Case")
public final class TitleCaseAction implements ActionListener {

    @Override
    public void actionPerformed(ActionEvent e) {
        //JOptionPane.showMessageDialog(null, "Title Case Executed");
        //JTextComponent ed = org.netbeans.api.editor.EditorRegistry.lastFocusedComponent();
        //Document doc = ed.getDocument();
        
        org.netbeans.api.editor.EditorRegistry.lastFocusedComponent().getCaretPosition();

                /*
        Node[] n = TopComponent.getRegistry().getActivatedNodes();
        if (n.length == 1) {
            EditorCookie ec = (EditorCookie) n[0].getCookie(EditorCookie.class);
            if (ec != null) {
                JEditorPane[] panes = ec.getOpenedPanes();
                if (panes.length > 0) {
                    int cursor = panes[0].getCaret().getDot();
                    String selection = panes[0].getSelectedText();
                    // USE selection
                }
            }
        }
        */
    }
}
