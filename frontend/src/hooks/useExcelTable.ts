import { useState, useMemo } from 'react';

export interface ColumnConfig {
  key: string;
  type: 'string' | 'number';
  getValue?: (item: any) => any;
}

export function useExcelTable(rawData: any[], columns: ColumnConfig[]) {
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [sortField, setSortField] = useState<string | null>(null);
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc' | null>(null);

  // Compute validation errors based on filters
  const validationErrors = useMemo(() => {
    const errors: Record<string, string> = {};
    columns.forEach((col) => {
      const filterVal = filters[col.key];
      if (!filterVal) return;

      if (col.type === 'number') {
        // Excel-like numeric validation: allow digits, decimals, negative signs, spaces, and operators <, >, =
        // If there are letters or invalid characters, flag it.
        const invalidChars = /[^\d<>=\s\.\-]/g;
        if (invalidChars.test(filterVal)) {
          errors[col.key] = 'Solo números u operadores (<, >, =)';
        }
      }
    });
    return errors;
  }, [filters, columns]);

  // Handle filter changes
  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  // Toggle sorting: asc -> desc -> none
  const handleSort = (key: string) => {
    if (sortField === key) {
      if (sortDirection === 'asc') {
        setSortDirection('desc');
      } else if (sortDirection === 'desc') {
        setSortField(null);
        setSortDirection(null);
      } else {
        setSortDirection('asc');
      }
    } else {
      setSortField(key);
      setSortDirection('asc');
    }
  };

  // Clear all sorting and filtering states
  const clearFilters = () => {
    setFilters({});
    setSortField(null);
    setSortDirection(null);
  };

  // Compute filtered and sorted data
  const filteredAndSortedData = useMemo(() => {
    let result = [...rawData];

    // 1. Apply filtering
    columns.forEach((col) => {
      const filterVal = filters[col.key]?.trim();
      if (!filterVal) return;

      // If the column has a validation error, we skip filtering with it or do a simple fallback.
      // Skipping/ignoring invalid numeric inputs mimics Excel's behavior where invalid input doesn't crash.
      if (validationErrors[col.key]) return;

      const getValue = col.getValue || ((item: any) => item[col.key]);

      result = result.filter((item) => {
        const rawVal = getValue(item);
        if (rawVal === undefined || rawVal === null) return false;

        if (col.type === 'number') {
          const numVal = Number(rawVal);
          
          // Parse operators if any
          const operatorMatch = filterVal.match(/^([<>]=?|=)\s*(-?\d*\.?\d*)$/);
          if (operatorMatch) {
            const op = operatorMatch[1];
            const targetNum = Number(operatorMatch[2]);
            if (isNaN(targetNum)) return true; // incomplete number, skip filter

            switch (op) {
              case '>': return numVal > targetNum;
              case '<': return numVal < targetNum;
              case '>=': return numVal >= targetNum;
              case '<=': return numVal <= targetNum;
              case '=': return numVal === targetNum;
              default: return true;
            }
          }

          // If no operator, check if the number contains the digits typed (substring-like search)
          // or is equal to the number.
          return numVal.toString().includes(filterVal);
        } else {
          // String filter: case-insensitive match
          return rawVal.toString().toLowerCase().includes(filterVal.toLowerCase());
        }
      });
    });

    // 2. Apply sorting
    if (sortField && sortDirection) {
      const col = columns.find((c) => c.key === sortField);
      const getValue = col?.getValue || ((item: any) => item[sortField]);
      const isNumber = col?.type === 'number';

      result.sort((a, b) => {
        const valA = getValue(a);
        const valB = getValue(b);

        if (valA === undefined || valA === null) return 1;
        if (valB === undefined || valB === null) return -1;

        if (isNumber) {
          const numA = Number(valA);
          const numB = Number(valB);
          return sortDirection === 'asc' ? numA - numB : numB - numA;
        } else {
          const strA = valA.toString();
          const strB = valB.toString();
          const comparison = strA.localeCompare(strB, undefined, { sensitivity: 'base', numeric: true });
          return sortDirection === 'asc' ? comparison : -comparison;
        }
      });
    }

    return result;
  }, [rawData, columns, filters, sortField, sortDirection, validationErrors]);

  return {
    filteredAndSortedData,
    filters,
    validationErrors,
    sortField,
    sortDirection,
    handleFilterChange,
    handleSort,
    clearFilters,
  };
}
