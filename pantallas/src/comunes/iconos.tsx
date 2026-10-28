// Iconos de Hugeicons, trazo redondeado (elegidos por Javier el 27 de octubre de 2026).
// Cada pantalla usa el nombre de aquí, no el de Hugeicons: si se cambia la biblioteca otra
// vez, solo cambia este archivo. Solo se importan los iconos que usa Vitalia.
import {
  Add01Icon,
  ArrowDataTransferHorizontalIcon,
  ArrowLeft01Icon,
  ArrowLeft02Icon,
  ArrowRight01Icon,
  ArrowRight02Icon,
  Calendar03Icon,
  CalendarAdd02Icon,
  CalendarCheckIn01Icon,
  CallIcon,
  Camera01Icon,
  Cancel01Icon,
  Clock01Icon,
  CreditCardIcon as TarjetaDeCredito,
  Delete02Icon,
  File02Icon,
  Home01Icon,
  IdentityCardIcon,
  Image01Icon,
  InformationCircleIcon,
  Location01Icon,
  Logout01Icon,
  Mail01Icon,
  Search01Icon,
  SecurityCheckIcon,
  SentIcon,
  SlidersHorizontalIcon as Deslizadores,
  SparklesIcon,
  SquareLock02Icon,
  Stethoscope02Icon,
  Task01Icon,
  Tick02Icon,
  Upload04Icon,
  UserAdd01Icon,
  UserGroupIcon,
  UserIcon as Persona,
  UserRemove01Icon,
  ViewIcon,
  ViewOffSlashIcon,
} from "@hugeicons/core-free-icons";
import { HugeiconsIcon, type IconSvgElement } from "@hugeicons/react";
import type { SVGProps } from "react";

type Propiedades = Omit<SVGProps<SVGSVGElement>, "ref" | "strokeWidth" | "color"> & {
  /** "bold" engruesa el trazo: para flechas, más y cerrar dentro de botones. */
  weight?: "regular" | "bold";
  size?: number;
};

function icono(dibujo: IconSvgElement, nombre: string) {
  function Icono({ weight = "regular", size = 22, ...resto }: Propiedades) {
    return (
      <HugeiconsIcon
        icon={dibujo}
        size={size}
        strokeWidth={weight === "bold" ? 2 : 1.6}
        color="currentColor"
        {...resto}
      />
    );
  }
  Icono.displayName = nombre;
  return Icono;
}

export const ArrowLeftIcon = icono(ArrowLeft02Icon, "ArrowLeftIcon");
export const ArrowRightIcon = icono(ArrowRight02Icon, "ArrowRightIcon");
export const ArrowsLeftRightIcon = icono(ArrowDataTransferHorizontalIcon, "ArrowsLeftRightIcon");
export const CalendarBlankIcon = icono(Calendar03Icon, "CalendarBlankIcon");
export const CalendarCheckIcon = icono(CalendarCheckIn01Icon, "CalendarCheckIcon");
export const CalendarPlusIcon = icono(CalendarAdd02Icon, "CalendarPlusIcon");
export const CameraIcon = icono(Camera01Icon, "CameraIcon");
export const CaretLeftIcon = icono(ArrowLeft01Icon, "CaretLeftIcon");
export const CaretRightIcon = icono(ArrowRight01Icon, "CaretRightIcon");
export const CheckIcon = icono(Tick02Icon, "CheckIcon");
export const ClipboardTextIcon = icono(Task01Icon, "ClipboardTextIcon");
export const ClockIcon = icono(Clock01Icon, "ClockIcon");
export const CreditCardIcon = icono(TarjetaDeCredito, "CreditCardIcon");
export const EnvelopeSimpleIcon = icono(Mail01Icon, "EnvelopeSimpleIcon");
export const EyeIcon = icono(ViewIcon, "EyeIcon");
export const EyeSlashIcon = icono(ViewOffSlashIcon, "EyeSlashIcon");
export const FileTextIcon = icono(File02Icon, "FileTextIcon");
export const HouseIcon = icono(Home01Icon, "HouseIcon");
export const IdentificationCardIcon = icono(IdentityCardIcon, "IdentificationCardIcon");
export const ImageIcon = icono(Image01Icon, "ImageIcon");
export const InfoIcon = icono(InformationCircleIcon, "InfoIcon");
export const LockKeyIcon = icono(SquareLock02Icon, "LockKeyIcon");
export const MagnifyingGlassIcon = icono(Search01Icon, "MagnifyingGlassIcon");
export const MapPinIcon = icono(Location01Icon, "MapPinIcon");
export const PaperPlaneRightIcon = icono(SentIcon, "PaperPlaneRightIcon");
export const PhoneIcon = icono(CallIcon, "PhoneIcon");
export const PlusIcon = icono(Add01Icon, "PlusIcon");
export const ShieldCheckIcon = icono(SecurityCheckIcon, "ShieldCheckIcon");
export const SignOutIcon = icono(Logout01Icon, "SignOutIcon");
export const SlidersHorizontalIcon = icono(Deslizadores, "SlidersHorizontalIcon");
export const SparkleIcon = icono(SparklesIcon, "SparkleIcon");
export const StethoscopeIcon = icono(Stethoscope02Icon, "StethoscopeIcon");
export const TrashIcon = icono(Delete02Icon, "TrashIcon");
export const UploadSimpleIcon = icono(Upload04Icon, "UploadSimpleIcon");
export const UserIcon = icono(Persona, "UserIcon");
export const UserMinusIcon = icono(UserRemove01Icon, "UserMinusIcon");
export const UserPlusIcon = icono(UserAdd01Icon, "UserPlusIcon");
export const UsersIcon = icono(UserGroupIcon, "UsersIcon");
export const XIcon = icono(Cancel01Icon, "XIcon");
