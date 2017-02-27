import javax.swing.table.*;
import java.util.*;

public class UserStats extends AbstractTableModel {
	private ArrayList<String> names;
	private ArrayList< ArrayList<String> > commits;
	public UserStats() {
		names = new ArrayList<String>();
		commits = new ArrayList< ArrayList<String> > ();
	}
	
	public void addName(String name) {
		names.add(name);
	}

	@Override
	public int getRowCount() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public int getColumnCount() {
		return names.size();
	}

	@Override
	public Object getValueAt(int rowIndex, int columnIndex) {
		return null;
	}
}
