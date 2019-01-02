/*
 * From given field names, build an object of their
 * empty error values also add common "_global" slot
 * errors unrelated to fields.
 *
 * Field errors are allways an array.
 *
 * Usage:
 *
 *  build_error_initials(["foo", "bar"]);
 *  >> { _global: [], foo: [], bar: [] }
 */
export function build_error_initials(fields){
    let initials = {
        "_global": []
    };

    fields.forEach(function(fieldname){
        initials[fieldname] = [];
    });

    return initials;
}
