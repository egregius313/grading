import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public abstract class App extends JFrame {
	public void buildMenu(String[] menus, Action[][] actions) {
		JMenuBar b = new JMenuBar();
		for (String menu : menus) {
			JMenu m = new JMenu(menu);
			b.add(m);
		}
		setJMenuBar(b);
	}
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
	
	public abstract void init();
	
	public App(String title, int w, int h, Color bg) {
		super(title);
		setSize(w,h);
		Container c = getContentPane();
		c.setBackground(bg);
		init();
		setVisible(true);
	}
}
