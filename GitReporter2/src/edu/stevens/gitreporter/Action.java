package edu.stevens.gitreporter;
import java.awt.event.*;

public class Action {
	private String text;
	private String name;
	private ActionListener action;
	private App app;
	public Action(App app, String t, String n, ActionListener a) {
		text = t; name = n; action = a;
		this.app = app;
		app.register(this);
	}
	public String getText() { return text; }
	public String getName() { return name; }
	public ActionListener getAction() { return action; }
	public void doIt() {
		ActionEvent e = new ActionEvent(app, 10000000, name);
		action.actionPerformed(e);
	}
	
		

}
