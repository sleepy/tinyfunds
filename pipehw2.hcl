// rss5pa pipehw2.hcl

########## the PC and condition codes registers #############
register fF { pc:64 = 0; }  // f_pc and F_pc are the PREDICTED PC register values

register cC { SF:1 = 0; ZF:1 = 1;} // default values 0 and 1 for SF & ZF

stall_C = (E_icode != OPQ); // condition codes are maintained if execute command not OPq


########## PC Update & Fetch #############
pc = [
    mispredicted : M_valP; // if there was a jump misprection, set current pc to instr after bad JXX
    1 : F_pc;              // otherwise, continue as normal

];

f_icode = i10bytes[4..8];
f_ifun = i10bytes[0..4];
f_rA = i10bytes[12..16]; 
f_rB = i10bytes[8..12];

f_valC = [
	f_icode in { JXX, CALL } : i10bytes[8..72];
	1 : i10bytes[16..80];
];

wire offset:64; // define temporary wire used

offset = [
	f_icode in { HALT, NOP, RET } : 1;
	f_icode in { RRMOVQ, OPQ, PUSHQ, POPQ } : 2;
	f_icode in { JXX, CALL } : 9;
	1 : 10;
];
f_valP = F_pc + offset; // **Note: Using f_valP twice here, not sure why valP needs to be carried over to decode just yet

f_pc = [
    f_icode == HALT : pc; // keep same instruction (prevent program from moving forward, i.e. stalling)
    loadUse : pc; // loaduse keeps same instruction (effectively stalling)
    f_icode in { JXX, CALL } : f_valC; // assumes all jumps are taken, all CALL calls are always taken

    1: f_valP; // other update PC register
];

f_stat = [
	f_icode == HALT : STAT_HLT;
	f_icode > 0xb : STAT_INS;
	1 : STAT_AOK;
];

// Pipline REG Fetch -> Decode //
register fD {
    stat:3 = STAT_AOK;
    icode:4 = NOP;
    ifun:4 = 0;
    rA:4 = REG_NONE;
    rB:4 = REG_NONE;
    valC:64 = 0;
    valP:64 = 0;
}


########## Decode #############

# source selection
reg_srcA = [
	D_icode in {RRMOVQ, OPQ} : D_rA; 
    D_icode in {RMMOVQ} : D_rA;
	1 : REG_NONE;
];

reg_srcB = [
    D_icode in {OPQ} : D_rB;
    D_icode in {RMMOVQ, MRMOVQ} : D_rB;
    1 : REG_NONE;
];

d_stat = D_stat;
d_icode = D_icode;
d_ifun = D_ifun;
d_valC = D_valC;
d_valP = D_valP;

d_valA = [	// MUX to handle rrmovq and irmovq Data Hazard from pipeLab1
       (e_icode in {IRMOVQ, OPQ}) && (e_dstE == reg_srcA) && (e_dstE != REG_NONE) : e_valE;               // previous inst destination, get value from ALU
       (m_icode in {IRMOVQ, OPQ}) && (m_dstE == reg_srcA) && (m_dstE != REG_NONE) : m_valE;
       (W_icode in {IRMOVQ, OPQ}) && (reg_dstE == reg_srcA) && (reg_dstE != REG_NONE): reg_inputE;        // handles ir mr lab hazzard

       (e_icode == RRMOVQ) && (e_dstE == reg_srcA) && (e_dstE != REG_NONE) : e_valA;  
       (m_icode == RRMOVQ) && (m_dstE == reg_srcA) && (m_dstE != REG_NONE) : m_valA;
       (W_icode == RRMOVQ) && (reg_dstE == reg_srcA) && (reg_dstE != REG_NONE): W_valA;    

       (m_icode in {MRMOVQ}) && (m_dstE == reg_srcA) && (m_dstE != REG_NONE) : m_valM;  // memory pipelab2 forwarding
       (W_icode in {MRMOVQ}) && (W_dstE == reg_srcA) && (W_dstE != REG_NONE) : W_valM;  // writeback pipelab2 forwarding


       1: reg_outputA; // all other cases so far are from normal output
       ];

d_valB = [
    (e_icode in {IRMOVQ, OPQ}) && (e_dstE == reg_srcB) && (e_dstE != REG_NONE) : e_valE;               // previous inst destination, get value from ALU
    (m_icode in {IRMOVQ, OPQ}) && (m_dstE == reg_srcB) && (m_dstE != REG_NONE) : m_valE;
    (W_icode in {IRMOVQ, OPQ}) && (reg_dstE == reg_srcB) && (reg_dstE != REG_NONE): reg_inputE;        // handles ir mr lab hazzard

    (e_icode == RRMOVQ) && (e_dstE == reg_srcB) && (e_dstE != REG_NONE) : e_valA;  
    (m_icode == RRMOVQ) && (m_dstE == reg_srcB) && (m_dstE != REG_NONE) : m_valA;
    (W_icode == RRMOVQ) && (reg_dstE == reg_srcB) && (reg_dstE != REG_NONE): W_valA;  

    (m_icode in {MRMOVQ}) && (m_dstE == reg_srcB) && (m_dstE != REG_NONE) : m_valM;  // memory pipelab2 forwarding
    (W_icode in {MRMOVQ}) && (W_dstE == reg_srcB) && (W_dstE != REG_NONE) : W_valM;  // writeback pipelab2 forwarding

   1: reg_outputB;
];

/* Load-Use Hazard Handling */
wire loadUse:1; // boolean true/false wire for detecting load-use condition

loadUse = [ /* True when MRmovq in Execute with its destination regiser == srcX is in decode   */
    (E_icode == MRMOVQ) && (E_dstE == reg_srcA) && (E_dstE != REG_NONE) : 1; // Load use hazard case
    (E_icode == MRMOVQ) && (E_dstE == reg_srcB) && (E_dstE != REG_NONE) : 1; // Load use hazard case
    1 : 0; //otherwise, no loadUse Hazard
];

// **NOTE: Stall F handling is done Above with PC register //
stall_D = loadUse; // keep same isntruction in decode one more cycle
bubble_E = loadUse || mispredicted; // nop send to the next execute stage for for the next cycle (prevent repeat instruction) & JXX squashing
bubble_M = mispredicted; // JXX squashing

d_dstE = [ /* can also be reg_dstM, but hw easys easier with dstE for RM/MRmovq */
	D_icode in {IRMOVQ, RRMOVQ, OPQ} : D_rB;
    D_icode in {MRMOVQ} : D_rA;
	1 : REG_NONE;
];


// Pipeline REG decode -> Execute //
register dE {
	stat:3 = STAT_AOK;
    icode:4 = NOP;
    ifun:4 = 0;
    valP:64 = 0;    // valP passed up to handle JXX
    valC:64 = 0;
    valA:64 = 0;
    valB:64 = 0;        
    dstE:4 = REG_NONE; 
   // dstM:4 = REG_NONE;  // TODO: uncomment after implementation
 } 

########## Execute #############

e_stat = E_stat;
e_icode = E_icode;
e_valP = E_valP;
e_valA = E_valA;
e_dstE = [ # Destination execute handling
    (E_icode == CMOVXX) && (!conditionsMet) : REG_NONE;    // CMOV (rrmov) case
    1: E_dstE;                                              // Usual case

];

//e_dstM = E_dstM; # TODO: uncomment when implemented

e_valE = [
    E_icode in {IRMOVQ} : E_valC;                                       // valE is just valC for IRMOVQ
    (E_icode == OPQ) && (E_ifun == ADDQ ): E_valA + E_valB;             // OPQ_ADDQ is addition of valA and val B
    (E_icode == OPQ) && (E_ifun == SUBQ ): E_valB - E_valA;             // OPQ_SUBQ is subtraction of valB from valB
    (E_icode == OPQ) && (E_ifun == ANDQ ): E_valA & E_valB;             // OPQ_ANDQ is bitwise and of valB and valA
    (E_icode == OPQ) && (E_ifun == XORQ ): E_valA ^ E_valB;             // OPQ_XORQ is bitwise xor of valB and valA
     E_icode in {RMMOVQ, MRMOVQ} : E_valB + E_valC;                      // RM MR movq compute memory addresses

    1: 0;                                                               // default value is 0 in event unused
];

# Update Condition codes on an OPQ instruction ONLY

c_ZF = (e_valE == 0);
c_SF = (e_valE >= 0x8000000000000000); // if value is negative

# Conditions Handling

wire conditionsMet:1; 
conditionsMet = [
	      mispredicted : M_Cnd;              // if there was a misprediction, reset the conditions met register to what it was last instruction
          E_ifun == ALWAYS : 1;              // true if ifun is zero, unconditional mov
	      E_ifun == LE : C_SF || C_ZF;       // ifun is 1 is Lesseq
	      E_ifun == LT : C_SF && (!C_ZF);    //ifun is 2 is Less
	      E_ifun == EQ : C_ZF; 	       // ifun is 3 is equal
	      E_ifun == NE : !C_ZF;  	       // ifun is 4 is not eqal
	      E_ifun == GE : (!C_SF) || C_ZF;    // ifun is 5 is greater or equal
	      E_ifun == GT : (!C_SF) && (!C_ZF); // ifun is 6 is greater

	      1 : 0; // conditions not met if something wrong
];

e_Cnd = conditionsMet; // store result of conditions for memory stage


//Pipeline REG execute -> Memory
register eM {
    stat:3 = STAT_AOK;
    icode:4 = NOP;
    Cnd:1 = 0;          // Condition codes, from page 424 in textbook, default 1. Handles JXX misprediction condition check timing hazard.
    valP:64 = 0;        // valP passed up to handle JXX
    valE:64 = 0;       
    valA:64 = 0;
    dstE:4 = REG_NONE; 
    //dstM:4 = REG_NONE;  # TODO: uncomment after implementation
}

########## Memory #############

wire mispredicted:1; // determines mispredict is current icode is JXX and condition code Cnd is 0
mispredicted = [
    ((M_icode == JXX) && (M_Cnd == 0)) : 1;       // conditions not met for JXX jump as based on execute state timing
    1 : 0;                                      // otherwise, not a misprediction
];

m_stat = M_stat;
m_icode = M_icode;
m_valE = M_valE;
m_valA = M_valA;
m_dstE = M_dstE;
//m_dstM = M_dstM;

#Handle writing and reading memory
mem_readbit = [
	    M_icode == 5 : 1;     // mrmovq needs to read
	    M_icode == POPQ : 1;  // POPQ requires reading
	    M_icode == RET : 1 ;  // ret needs to read next address

	    1 : 0;                // DEFAULT: don't read
];
mem_writebit = [
	   M_icode == 4 : 1;      // writing required for RMMOVQ
	   M_icode == PUSHQ: 1;   // writing required for PUSHQ
	   M_icode == CALL: 1;    // writing required for call
	   1 : 0;               // DEFAULT don't write memory
];

# mem_addr is the 64 bit value if either bit above is flagged as 1
mem_addr = [
	 (M_icode == 4) || (M_icode == 5) : M_valE;  //memory addres to write for RMMOVQ & MRmovq
	 M_icode == PUSHQ : M_valE;                // should be rsp -8 value
	 //M_icode == POPQ: reg_outputB;            #TODO: uncomment after implementation // set address to pre-add rsp address
	 M_icode == CALL : M_valE;                 // call writes to the stack
	 //M_icode == RET: reg_outputB;              // set address to read from as pre-added rsp address (bytes still exist there)
	 
     1 : 0;                                  #TODO: uncomment after implementation // default value is 0 i.e. no address selected.
];

mem_input = [
	  M_icode == RMMOVQ : M_valA;     // valE has computed mem addr. rA is value to write
	  M_icode == PUSHQ : M_valA;  // value of rA is written to mem addr rsp - 8.
	  // M_icode == CALL : (P_pc + 9);   // value of instruction after call into  memory (call is 9 bytes long)
	  1 : 0;                        // shouldn't write it writebit is 0, by default
];

// valM = value read from memory
m_valM = [
    M_icode in {MRMOVQ} : mem_output; //read value in memory to put into register

    1 : 0; // nothing read from memory
];




// Pipeline REG memory -> Writeback
register mW{
    stat:3 = STAT_AOK;
    icode:4 = NOP;
    valE:64 = 0;
    valM:64 = 0;          #TODO: uncomment after implementation
    valA:64 = 0;            // NOTE: this is not in textbook processor, seems to be shared with valM, may require update
    dstE:4 = REG_NONE; 
    //dstM:4 = REG_NONE;    #TODO: uncomment after implementation
}


########## Writeback #############


# destination selection
reg_dstE = W_dstE;

reg_inputE = [ # unlike book, we handle the "forwarding" actions (something + 0) here
	W_icode == RRMOVQ : W_valA;              // W_valA = reg_outputA
	W_icode in {IRMOVQ, OPQ} : W_valE;       // valE is just valC for IRMOVQ, valE is valA+valB for OPQ
    W_icode in {MRMOVQ} : W_valM;            // take value from memory into rA for MRMOVQ
        1: 0xBADBADBAD;                      // I assume for testing purposes
];


########## Status updates #############

Stat = W_stat;




