import { isUndefined } from "@carefree0910/core";

import type { IDefinitions } from "@/schema/fields";
import TextField from "./TextField";
import NumberField from "./NumberField";
import SelectField from "./SelectField";

export function useDefinitions(definitions: IDefinitions, numColumns?: number) {
  const nc = numColumns ?? 1;

  return (
    <>
      {Object.entries(definitions).map(([field, definition]) => {
        let Field: any | null = null;
        if (definition.type === "text") {
          Field = TextField;
        } else if (definition.type === "number") {
          Field = NumberField;
        } else if (definition.type === "select") {
          Field = SelectField;
        }
        if (!Field) return null;
        const props = definition.props ?? {};
        if (isUndefined(props.h)) props.h = "42px";
        if (isUndefined(props.w)) {
          props.w = numColumns === 1 ? "100%" : `${(100 - 5 * (nc - 1)) / nc}%`;
        }
        definition.props = props;
        return <Field key={field} field={field} definition={definition} />;
      })}
    </>
  );
}
