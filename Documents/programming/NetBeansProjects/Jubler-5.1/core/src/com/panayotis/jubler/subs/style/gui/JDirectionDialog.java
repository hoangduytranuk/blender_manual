/*
 * JDirectionDialog.java
 *
 * Created on 7 Σεπτέμβριος 2005, 1:16 μμ
 *
 * This file is part of Jubler.
 *
 * Jubler is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, version 2.
 *
 *
 * Jubler is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jubler; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */

package com.panayotis.jubler.subs.style.gui;

import com.panayotis.jubler.JubFrame;
import com.panayotis.jubler.subs.style.SubStyle.Direction;
import java.awt.MouseInfo;
import java.awt.Point;
import javax.swing.Icon;
import javax.swing.JWindow;

/**
 *
 * @author teras
 */
public class JDirectionDialog extends JWindow {

    private JDirection direction;

    /**
     * Creates new form JDirectionDIalog
     */
    public JDirectionDialog(JubFrame parent) {
        super(parent);
        initComponents();
        direction = new JDirection();
        add(direction);
        pack();
    }

    public void setVisible(boolean isVisible) {
        super.setVisible(isVisible);
        if (isVisible) {
            Point where = MouseInfo.getPointerInfo().getLocation();
            int width = getWidth();
            int height = getHeight();
            where.x -= width / 6 + direction.getControlX() * width / 3;
            where.y -= height / 6 + direction.getControlY() * height / 3;
            setLocation(where);
            direction.requestFocusInWindow();
        }
    }

    public Direction getDirection() {
        return direction.getDirection();
    }

    public Icon getIcon() {
        return direction.getIcon();
    }

    public Icon getIcon(Direction d) {
        return direction.getIcon(d);
    }

    public void setListener(DirectionListener listener) {
        direction.setListener(listener);
    }

    public void setDirection(Direction d) {
        direction.setDirection(d);
    }

    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    // <editor-fold defaultstate="collapsed" desc=" Generated Code ">//GEN-BEGIN:initComponents
    private void initComponents() {

        addFocusListener(new java.awt.event.FocusAdapter() {
            public void focusLost(java.awt.event.FocusEvent evt) {
                formFocusLost(evt);
            }
        });

    }
    // </editor-fold>//GEN-END:initComponents

    private void formFocusLost(java.awt.event.FocusEvent evt) {//GEN-FIRST:event_formFocusLost
        setVisible(false);
    }//GEN-LAST:event_formFocusLost
    // Variables declaration - do not modify//GEN-BEGIN:variables
    // End of variables declaration//GEN-END:variables
}
