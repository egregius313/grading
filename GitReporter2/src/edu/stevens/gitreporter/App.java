package edu.stevens.gitreporter;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
/**
 * 
 * @author dkruger
 * 
 * General parent for windowing applications to simplify size, menus, toolbars 
 * and other user interface code
 * 
 * To use this, write your own subclass and write methods init(), buildMenu()...
 */
public abstract class App extends JFrame {
	private boolean dirty; // if dirty is true, some state should be saved before quitting

	/**
	 * Build a menubar with menus and submenus connected to actions
	 * @param menus
	 * @param actions
	 */
	public void buildMenu(String[] menus, Action[][] actions) {
//		int c = 2;
//		c++; // add one to c  DON'T COMMENT LIKE THIS!!!
		JMenuBar b = new JMenuBar();
		for (int i = 0; i < menus.length; ++i) {
			JMenu m = new JMenu(menus[i]);
			b.add(m);
			if (actions[i] != null) { // in case the programmer passes in a temporary null menu, don't crash
				for (int j = 0; j < actions[i].length; ++j) {
					JMenuItem item = new JMenuItem(actions[i][j].getText());
					item.addActionListener(actions[i][j].getAction());
					m.add(item);
				}
			}
		}
		setJMenuBar(b);
	}
	/**
	 * Create a horizontal toolbar at the top of the window with variable sized icons attached to buttons.
	 * @param iconSize
	 * @param c
	 * @param actions
	 */
	public void toolBar(int iconSize, Color c, Action... actions) {
		int w = getWidth();
		int cols = w / iconSize;
		int rows = actions.length / cols + 1;
		JPanel p = new JPanel();
		p.setBackground(c);
		p.setLayout(new GridLayout(rows, cols));
		//System.out.println(rows + "," + cols);
		for (Action a : actions) {
			String iconName = "img/" + a.getText();
			ImageIcon icon = new ImageIcon(iconName);
			//System.out.println(icon);
			JButton b = new JButton(icon);
			b.addActionListener(a.getAction());
			p.add(b);
		}
		Container cnt = getContentPane();
		cnt.add(BorderLayout.NORTH, p);
	}
	public void register(Action a) {

	}
	public void setDirty(boolean b) {
		dirty = b;
	}
	
	public abstract void init();
	
	public App(String title, int w, int h, Color bg) {
		super(title);
		setSize(w,h);
		Container c = getContentPane();
		c.setBackground(bg);
		dirty = false;
		init();
		setVisible(true);
	}
	public abstract void save();
	public void requestQuit() {
		if (!dirty)
			System.exit(0);
		 int result = JOptionPane.showConfirmDialog((Component) null,
				 "Save first?",
			        "alert", JOptionPane.OK_CANCEL_OPTION);
		 if (result == JOptionPane.NO_OPTION) {
		    System.out.println("No button clicked");
		 } else if (result == JOptionPane.YES_OPTION) {
			 save();
		 } else {
		    System.exit(0);
		 }
		 
	}
}
