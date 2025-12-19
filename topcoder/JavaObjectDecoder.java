import java.io.*;
import java.util.*;
import java.util.Base64;

/**
 * Java program to decode base64 encoded Java serialized objects and print their string representation.
 * Usage: java JavaObjectDecoder <base64_encoded_string>
 */
public class JavaObjectDecoder {
    
    public static void main(String[] args) {
        if (args.length != 1) {
            System.err.println("Usage: java JavaObjectDecoder <base64_encoded_string>");
            System.exit(1);
        }
        
        String base64String = args[0];
        
        try {
            // Decode base64
            byte[] decodedBytes = Base64.getDecoder().decode(base64String);
            
            // Deserialize Java object
            ByteArrayInputStream bais = new ByteArrayInputStream(decodedBytes);
            ObjectInputStream ois = new ObjectInputStream(bais);
            Object obj = ois.readObject();
            ois.close();
            
            // Print proper string representation
            String result = objectToString(obj);
            System.out.println(result);
            
        } catch (Exception e) {
            System.err.println("Error decoding object: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
    
    /**
     * Convert an object to its proper string representation.
     * Handles arrays, collections, and other objects appropriately.
     */
    private static String objectToString(Object obj) {
        if (obj == null) {
            return "null";
        }
        
        // Handle arrays
        if (obj.getClass().isArray()) {
            return arrayToString(obj);
        }
        
        // Handle collections
        if (obj instanceof Collection) {
            Collection<?> collection = (Collection<?>) obj;
            StringBuilder sb = new StringBuilder();
            sb.append("[");
            boolean first = true;
            for (Object item : collection) {
                if (!first) {
                    sb.append(", ");
                }
                sb.append(objectToString(item));
                first = false;
            }
            sb.append("]");
            return sb.toString();
        }
        
        // Handle maps
        if (obj instanceof Map) {
            Map<?, ?> map = (Map<?, ?>) obj;
            StringBuilder sb = new StringBuilder();
            sb.append("{");
            boolean first = true;
            for (Map.Entry<?, ?> entry : map.entrySet()) {
                if (!first) {
                    sb.append(", ");
                }
                sb.append(objectToString(entry.getKey()));
                sb.append("=");
                sb.append(objectToString(entry.getValue()));
                first = false;
            }
            sb.append("}");
            return sb.toString();
        }

        if (obj instanceof String) {
            return "\"" + obj.toString() + "\"";
        }
        
        // For all other objects, use toString()
        return obj.toString();
    }
    
    /**
     * Convert array to string using Arrays.toString() for appropriate types.
     */
    private static String arrayToString(Object array) {
        Class<?> componentType = array.getClass().getComponentType();
        
        if (componentType == boolean.class) {
            return Arrays.toString((boolean[]) array);
        } else if (componentType == byte.class) {
            return Arrays.toString((byte[]) array);
        } else if (componentType == char.class) {
            return Arrays.toString((char[]) array);
        } else if (componentType == double.class) {
            return Arrays.toString((double[]) array);
        } else if (componentType == float.class) {
            return Arrays.toString((float[]) array);
        } else if (componentType == int.class) {
            return Arrays.toString((int[]) array);
        } else if (componentType == long.class) {
            return Arrays.toString((long[]) array);
        } else if (componentType == short.class) {
            return Arrays.toString((short[]) array);
        } else {
            // Object array
            Object[] objArray = (Object[]) array;
            StringBuilder sb = new StringBuilder();
            sb.append("[");
            for (int i = 0; i < objArray.length; i++) {
                if (i > 0) {
                    sb.append(", ");
                }
                sb.append(objectToString(objArray[i]));
            }
            sb.append("]");
            return sb.toString();
        }
    }
}