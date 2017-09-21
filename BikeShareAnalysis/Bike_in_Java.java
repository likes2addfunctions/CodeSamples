import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.Object;
import java.util.*;
import java.text.*;
import com.csvreader.CsvReader;

public class Bike_in_Java {
	private static List get_date_range(String start_string, String end_string) {
		// System.out.println(start_string + " " + end_string);
		List Date_Range = new ArrayList();
		DateFormat df = new SimpleDateFormat("MM/dd/yyyy");
		Date start_date;
		Date end_date;
		Date next_date;
		try {
			start_date = df.parse(start_string);
			end_date = df.parse(end_string);
			Calendar c = Calendar.getInstance();
			next_date = start_date;
			int comp_int = next_date.compareTo(end_date);
			while (comp_int <= 0) {
				Date_Range.add(df.format(next_date));
				c.setTime(next_date);
				c.add(Calendar.DATE, 1);
				next_date = c.getTime();
				comp_int = next_date.compareTo(end_date);
			}
		}
		catch (Exception e) {
		}	
		return (Date_Range);
	}
	private static void add_update(Map dict, String key, String val) {
		if (dict.get(key) != null) {
			dict.put(key, Double.valueOf(dict.get(key).toString()) + Double.valueOf(val));
		}
				
		else {
			dict.put(key, Double.valueOf(val));
		}
	}
	public static void main(String[] args) {		
		try {			
			Set Bikes = new HashSet();
			Set Dates = new HashSet();
			Map<String, Double> Rides_by_bike = new HashMap<String, Double>();
			Map<String, Double> Rides_by_date = new HashMap<String, Double>();
			int num_of_trips = 0;
			int num_of_round_trips = 0;
			CsvReader trips = new CsvReader("201508_trip_data.csv");
			trips.readHeaders();
			while (trips.readRecord()) {
				num_of_trips ++;
				String Trip_ID = trips.get("Trip_ID");
				String Duration = trips.get("Duration");
				String Start_Date = trips.get("Start_Date");
				String Start_Station = trips.get("Start_Station");
				String Start_Terminal = trips.get("Start_Terminal");
				String End_Date = trips.get("End_Date");
				String End_Station = trips.get("End_Station");
				String End_Terminal = trips.get("End_Terminal");
				String Bike_No = trips.get("Bike_#");
				String Subscriber_Type = trips.get("Subscriber_Type");
				String Zip_Code = trips.get("Zip_Code");
				List date_range = get_date_range(Start_Date, End_Date);
				Bikes.add(Bike_No);
				add_update(Rides_by_bike,Bike_No,Duration);
				Iterator<String> date_range_it = date_range.iterator();
				while(date_range_it.hasNext()) {
					String this_date = date_range_it.next();
					Dates.add(this_date);
					add_update(Rides_by_date,this_date,"1");
				}
				if (Start_Station.equals(End_Station)) {
					num_of_round_trips ++;
				}				
			}
			trips.close();
			String max_time_bike = "";
 			Double max_duration = 0.0;
 			String curr_bike = "";	
 			Iterator<String> Bike_it = Bikes.iterator();
 			while(Bike_it.hasNext()) {	
 				curr_bike = Bike_it.next();
 				if (max_duration < Rides_by_bike.get(curr_bike)) {
 					max_duration = Rides_by_bike.get(curr_bike);
 					max_time_bike = curr_bike;
 				}
 			}
			List D_List = new ArrayList(Dates);
			Collections.sort(D_List);
			Iterator<String> Dates_it = D_List.iterator();
			String curr_date = "";
			while(Dates_it.hasNext()) {	
 				curr_date = Dates_it.next();
 				System.out.println(curr_date + "  " + Rides_by_date.get(curr_date));
 			}
 			System.out.println(max_time_bike + " was used for " + max_duration + " seconds.");
			System.out.println(num_of_round_trips + " round trips taken.");
			System.out.println(num_of_trips + " total trips taken");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

}
