/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package bitwise;

/**
 *
 * @author Hoang Duy Tran <hoangduytran@gmail.com>
 */
public class BitWise {

    /**
     * @param args the user command arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        int bitmask = 0x000f;
        int val = 0x2222;
        int and_op = bitmask & val;
        int or_op = bitmask | val;
        
        System.out.println(" and: " + and_op + " or: " + or_op);
        
        val = 0x80000000;
        int unsigned_shift_right = val >>> 1;
        int signed_shift_right = val >> 1;
        System.out.println("original:" + val + " unsigned_shift_right >>> 1: " + unsigned_shift_right + " signed_shift_right: " + signed_shift_right);
        
        unsigned_shift_right = val >>> 31;
        System.out.println(" original: " + val + " unsigned_shift_right = val >>> 31: " + unsigned_shift_right + " max int: " + Integer.MAX_VALUE);
        
        unsigned_shift_right = val >>> 32;
        System.out.println(" original: " + val + " unsigned_shift_right = val >>> 32: " + unsigned_shift_right + " max int: " + Integer.MAX_VALUE);

        unsigned_shift_right = val >>> 33;
        System.out.println(" original: " + val + " unsigned_shift_right = val >>> 33: " + unsigned_shift_right + " max int: " + Integer.MAX_VALUE);

        
        val = 0x1;
        int signed_shift_left = val << 31;
        System.out.println(" original: " + val + " shift_left<<31: " + signed_shift_left + " min int: " + Integer.MIN_VALUE);
    }
    
}
